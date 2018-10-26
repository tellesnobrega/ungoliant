import json
import os
import time

import clients


class CumulativeFlowJob(object):

    CACHE_PREFIX = os.path.join(clients.cache_dir, "cfj_")

    def __init__(self, bz_client=clients.bz_client):
        self.bz_client = bz_client

    def _get_cache_path(self, bug_id):
        return self.CACHE_PREFIX + str(bug_id)

    def _get_bug_from_cache(self, bug_id, cache_seconds=86400):
        path = self._get_cache_path(bug_id)
        if os.path.isfile(path):
            if os.path.getmtime(path) - time.time() < cache_seconds:
                with open(path, 'r') as fp:
                    return json.load(fp)

    def _get_bug_from_bz(self, bug_id):
        bug = clients.bz_client.getbug(bug_id, include_fields=['id'])
        raw_hx = bug.get_history_raw()
        for event in raw_hx['bugs'][0]['history']:
            event['when'] = time.mktime(event['when'].timetuple())
        with open(self._get_cache_path(bug_id), 'w') as fp:
            json.dump(raw_hx, fp)
        return raw_hx

    def get_raw_history(self, bug_id, cache_seconds=86400):
        hx = self._get_bug_from_cache(bug_id, cache_seconds)
        if not hx:
            hx = self._get_bug_from_bz(bug_id)
        return hx

    def get_state_hx(self, bug_ids, cache_seconds=86400):
        """Return state history for a sequence of bugs.

        Expects a sequence of bugzilla Bug objects.
        Returns history data as:
        {bug_id: {str(DateTime): bug_status, ...}, ...}
        """
        # TODO: Need to store create_date as a NEW status.
        state_hx = {}
        for bug_id in bug_ids:
            raw_hx = self.get_raw_history(bug_id, cache_seconds)
            raw_state_hx = {
                bug['id']: {
                    str(event['when']): [
                        change['added']
                        for change in event['changes']
                        if change['field_name'] == 'status'
                    ]
                    for event in bug['history']
                } for bug in raw_hx['bugs']
            }
            state_hx.update({
                id: {
                    time: status[0]
                    for time, status in history.items()
                    if len(status)
                }
                for id, history in raw_state_hx.items()
            })
        return state_hx
