import datetime
import uuid

STATUS_PENDING       = 'pending'
STATUS_IN_PROGRESS   = 'in_progress'
STATUS_DONE          = 'done'
STATUS_ERROR         = 'error'

class TaskStore:
    def __init__(self, db):
        self._db = db

    def create_indices(self):
        self._db['tasks'].create_index('task_id')
        self._db['tasks'].create_index('state')

    def get_status_report(self, task_id):
        task = self._db['tasks'].find_one(
            {'task_id' : task_id},
            {'status' : 1, 'error' : 1, 'result' : 1}
            )
        if task is None:
            return { 
                'status' : STATUS_ERROR,
                'error' : f'Task ID {task_id} not found.' 
                }
        else:
            report = { 'status' : task['status'] }
            for k in ['result', 'error']:
                if k in task:
                    report[k] = task[k]
            return report

    def create(self, flags, seed, metaconfig, **metadata):
        while True:
            task_id = str(uuid.uuid4())[:8]
            check_task = self._db['tasks'].find_one({'task_id' : task_id}, {'_id' : 1})
            if check_task is None:
                break

        #cherrypy.log(f"[Generator] starting new task {task_id} - flags: {flags}, seed: {seed}")
        now = datetime.datetime.utcnow()
        doc = {
            'task_id' : task_id,
            'status' : STATUS_PENDING,
            'flags' : flags,
            'seed' : seed,
            'startedTime' : now,
            'updatedTime' : now
            }
        if metaconfig:
            doc['metaconfig'] = metaconfig
        doc.update(metadata)
        self._db['tasks'].insert_one(doc)

        return task_id

    def report_status(self, task_id, status):
        self._db['tasks'].update_one(
            {'task_id' : task_id}, 
            {'$set' : {
                'status' : status,
                'updatedTime' : datetime.datetime.utcnow(),
            }})

    def report_error(self, task_id, error_info, **kwargs):
        set_values = {
            'status' : STATUS_ERROR, 
            'error' : error_info,
            'updatedTime' : datetime.datetime.utcnow(),
            }
        set_values.update(**kwargs)

        self._db['tasks'].update_one(
            {'task_id' : task_id},
            {'$set' : set_values}
            )

    def report_done(self, task_id, result):
        self._db['tasks'].update_one(
            {'task_id' : task_id},
            {'$set' : {
                'status' : STATUS_DONE, 
                'result' : result,
                'updatedTime' : datetime.datetime.utcnow(),
            }})

