# check if a stats db is available
try:
    # python3.7 -m pip install pip
    # pip3.7 install mysql-connector-python --user
    import mysql.connector
    from db_params import dbParams
    dbAvailable = True
except:
    dbAvailable = False

from utils.parameters import medium, hard, harder, hardcore, mania
from utils.utils import removeChars

class DB:
    def __init__(self):
        self.dbAvailable = dbAvailable
        if self.dbAvailable == False:
            return

        try:
            self.conn = mysql.connector.connect(**dbParams)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("DB.__init__::error connect/create cursor: {}".format(e))
            self.dbAvailable = False

    def close(self):
        if self.dbAvailable == False:
            return

        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("DB.close::error: {}".format(e))

    # to be used with 'with'
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def commit(self):
        if self.dbAvailable == False:
            return

        try:
            self.conn.commit()
        except Exception as e:
            print("DB.commit::error: {}".format(e))

    # write data
    def initSolver(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into solver (action_time) values (now());"
            self.cursor.execute(sql)
            return self.cursor.lastrowid
        except Exception as e:
            print("DB.initSolver::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addSolverParams(self, id, romFileName, preset, difficultyTarget, pickupStrategy, itemsForbidden):
        if self.dbAvailable == False or id == None:
            return

        try:
            sql = "insert into solver_params values (%d, '%s', '%s', %d, '%s');" % (id, romFileName, preset, difficultyTarget, pickupStrategy)
            self.cursor.execute(sql)

            sql = "insert into solver_items_forbidden values (%d, '%s');"
            for item in itemsForbidden:
                self.cursor.execute(sql % (id, item))
        except Exception as e:
            print("DB.addSolverParams::error execute: {}".format(e))
            self.dbAvailable = False

    def addSolverResult(self, id, returnCode, duration, result):
        if self.dbAvailable == False:
            return

        def lenNone(var):
            if var == None:
                return 0
            else:
                return len(var)

        try:
            if returnCode == 0:
                sql = "insert into solver_collected_items values (%d, '%s', %d);"
                for item, count in result['collectedItems'].items():
                    if count > 0:
                        self.cursor.execute(sql % (id, item, count))

                sql = "insert into solver_result values (%d, %d, %f, %d, %d, %d, %s, %d, %d, %d, %d, %d);" % (id, returnCode, duration, result['difficulty'], result['knowsUsed'][0], result['knowsUsed'][1], result['itemsOk'], lenNone(result['remainTry']), lenNone(result['remainMajors']), lenNone(result['remainMinors']), lenNone(result['skippedMajors']), lenNone(result['unavailMajors']))
            else:
                sql = "insert into solver_result (solver_id, return_code, duration) values (%d, %d, %f);" % (id, returnCode, duration)

            self.cursor.execute(sql)
        except Exception as e:
            print("DB.addSolverResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def initRando(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into randomizer (action_time) values (now());"
            self.cursor.execute(sql)
            return self.cursor.lastrowid
        except Exception as e:
            print("DB.initRando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addRandoParams(self, id, params):
        if self.dbAvailable == False:
            return None

        ignoreParams = ['paramsFileTarget', 'complexity']

        try:
            sql = "insert into randomizer_params values (%d, '%s', '%s');"
            for (name, value) in params.items():
                if name in ignoreParams:
                    continue
                self.cursor.execute(sql % (id, name, value))
        except Exception as e:
            print("DB.addRandoParams::error execute: {}".format(e))
            self.dbAvailable = False

    def updateRandoParams(self, id, params):
        if self.dbAvailable == False:
            return None

        try:
            sql = "update randomizer_params set value = '%s' where randomizer_id = %d and name = '%s';"
            for (name, value) in params.items():
                self.cursor.execute(sql % (value, id, name))
        except Exception as e:
            print("DB.updateRandoParams::error execute: {}".format(e))
            self.dbAvailable = False

    def addRandoResult(self, id, returnCode, duration, msg):
        if self.dbAvailable == False:
            return None

        def escapeMsg(msg):
            return msg.replace("'", "''")

        try:
            msg = escapeMsg(msg)
            sql = "insert into randomizer_result (randomizer_id, return_code, duration, error_msg) values (%d, %d, %f, '%s');"
            self.cursor.execute(sql % (id, returnCode, duration, msg))
        except Exception as e:
            print("DB.addRandoResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def addRandoUploadResult(self, id, guid, fileName):
        if self.dbAvailable == False:
            return None

        try:
            sql = """
update randomizer set upload_status = 'local', filename = '%s', guid = '%s'
where id = %s;"""
            self.cursor.execute(sql % (fileName, guid, id))
        except Exception as e:
            print("DB.addRandoUploadResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def addPresetAction(self, preset, action):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into preset_action (preset, action_time, action) values ('%s', now(), '%s');"
            self.cursor.execute(sql % (preset, action))
        except Exception as e:
            print("DB.initPresets::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addISolver(self, preset, type, romFileName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into isolver (init_time, preset, type, romFileName) values (now(), '%s', '%s', '%s');"
            self.cursor.execute(sql % (preset, type, romFileName))
        except Exception as e:
            print("DB.addISolver::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addSprite(self, sprite):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into sprites (init_time, sprite) values (now(), '%s');"
            self.cursor.execute(sql % (sprite, ))
        except Exception as e:
            print("DB.addSprite::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addPlandoRando(self, return_code, duration, msg):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into plando_rando (init_time, return_code, duration, error_msg) values (now(), %d, %f, '%s');"
            self.cursor.execute(sql % (return_code, duration, msg))
        except Exception as e:
            print("DB.addPlandoRando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    # read data
    def execSelect(self, sql, params=None):
        if self.dbAvailable == False:
            return None

        try:
            if params == None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql % params)
            return self.cursor.fetchall()
        except Exception as e:
            print("DB.execSelect::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def getUsage(self, table, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select date(action_time), count(*) from {} where action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK) group by date(action_time) order by 1;".format(table)
        return self.execSelect(sql, (weeks,))

    def getSolverUsage(self, weeks):
        return self.getUsage('solver', weeks)

    def getRandomizerUsage(self, weeks):
        return self.getUsage('randomizer', weeks)

    def getSolverPresets(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select distinct(sp.preset) from solver s join solver_params sp on s.id = sp.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK);"
        presets = self.execSelect(sql, (weeks,))
        if presets == None:
            return None

        # db returns tuples
        presets = [preset[0] for preset in presets]

        # pivot
        sql = "SELECT date(s.action_time)"
        for preset in presets:
            sql += ", SUM(CASE WHEN sp.preset = '{}' THEN 1 ELSE 0 END) AS count_{}".format(preset, preset)
        sql += " FROM solver s join solver_params sp on s.id = sp.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(s.action_time);".format(weeks)

        return (presets, self.execSelect(sql))

    def getSolverResults(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select date(s.action_time), sr.return_code, count(*) from solver s join solver_result sr on s.id = sr.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK) group by date(s.action_time), sr.return_code order by 1;"
        return self.execSelect(sql, (weeks,))

    def getSolverDurations(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select s.action_time, sr.duration from solver s join solver_result sr on s.id = sr.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK) order by 1;"
        return self.execSelect(sql, (weeks,))

    def getRandomizerPresets(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select distinct(value) from randomizer r join randomizer_params rp on r.id = rp.randomizer_id where rp.name = 'preset' and r.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK);"
        presets = self.execSelect(sql, (weeks,))
        if presets == None:
            return None

        # db returns tuples
        presets = [preset[0] for preset in presets]

        # pivot
        sql = "SELECT date(r.action_time)"
        for preset in presets:
            sql += ", SUM(CASE WHEN rp.value = '{}' THEN 1 ELSE 0 END) AS count_{}".format(preset, preset)
        sql += " FROM randomizer r join randomizer_params rp on r.id = rp.randomizer_id where rp.name = 'preset' and r.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(r.action_time);".format(weeks)

        return (presets, self.execSelect(sql))

    def getRandomizerDurations(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select r.action_time, rr.duration from randomizer r join randomizer_result rr on r.id = rr.randomizer_id where r.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK) order by 1;"
        return self.execSelect(sql, (weeks,))

    def getSolverData(self, weeks):
        if self.dbAvailable == False:
            return None

        # return all data csv style
        sql = """select sr.return_code, s.id, s.action_time,
sp.romFileName, sp.preset, sp.difficultyTarget, sp.pickupStrategy,
sr.return_code, lpad(round(sr.duration, 2), 5, '0'), sr.difficulty, sr.knows_used, sr.knows_known, sr.items_ok, sr.len_remainTry, sr.len_remainMajors, sr.len_remainMinors, sr.len_skippedMajors, sr.len_unavailMajors,
group_concat("(", sci.item, ", ", sci.count, ")" order by sci.item),
sif.forbidden_items
from solver s
  left join solver_params sp on s.id = sp.solver_id
  left join solver_result sr on s.id = sr.solver_id
  left join solver_collected_items sci on s.id = sci.solver_id
  left join (select solver_id, group_concat(item order by item) as forbidden_items from solver_items_forbidden group by solver_id) sif on s.id = sif.solver_id
where s.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK)
group by s.id
order by s.id;"""

        header = ["id", "actionTime", "romFileName", "preset", "difficultyTarget", "pickupStrategy", "returnCode", "duration", "difficulty", "knowsUsed", "knowsKnown", "itemsOk", "remainTry", "remainMajors", "remainMinors", "skippedMajors", "unavailMajors", "collectedItems", "forbiddenItems"]
        return (header, self.execSelect(sql, (weeks,)))

    def getRandomizerData(self, weeks):
        if self.dbAvailable == False:
            return None

        # now that we store random multi select values we reach a mysql limit with group_concat.
        # solution:
        # SET GLOBAL group_concat_max_len=8192;
        # but we're not super user on production, so set it at session level
        sql = "SET SESSION group_concat_max_len=8192";
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print("DB.getRandomizerData::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False
            return None

        sql = """select rr.return_code,
r.id, r.action_time, r.guid, rr.return_code, lpad(round(rr.duration, 2), 5, '0'), rr.error_msg,
group_concat("'", rp.name, "': '", rp.value, "'" order by rp.name)
from randomizer r
  left join randomizer_params rp on r.id = rp.randomizer_id
  left join randomizer_result rr on r.id = rr.randomizer_id
where r.action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK)
group by r.id
order by r.id;"""

        data = self.execSelect(sql, (weeks,))
        if data == None:
            return None

        outData = []
        paramsSet = set()
        for row in data:
            # use a dict for the parameters which are in the last column
            params = row[-1]
            dictParams = eval('{' + params + '}')
            outData.append(list(row[0:-1]) + [dictParams,])
            paramsSet.update(dictParams.keys())

            # keep guid only for non race seeds
            returnCodeColumn = 0
            guidColumn = 3
            if outData[-1][-1].get('raceMode', 'off') == 'on' or outData[-1][returnCodeColumn] != 0:
                # remove guid
                outData[-1][guidColumn] = ''
            else:
                # add link
                outData[-1][guidColumn] = '<a href="customizer/{}">permalink</a>'.format(outData[-1][guidColumn])

        # custom sort of the params
        paramsHead = []
        for param in ['seed', 'preset', 'startLocation', 'startLocationMultiSelect', 'areaRandomization', 'areaLayout', 'lightAreaRandomization', 'doorsColorsRando', 'allowGreyDoors', 'bossRandomization', 'minimizer', 'minimizerQty', 'minimizerTourian', 'majorsSplit', 'majorsSplitMultiSelect', 'scavNumLocs', 'scavRandomized', 'scavEscape', 'progressionSpeed', 'progressionSpeedMultiSelect', 'maxDifficulty', 'morphPlacement', 'morphPlacementMultiSelect', 'suitsRestriction', 'energyQty', 'energyQtyMultiSelect', 'minorQty', 'missileQty', 'superQty', 'powerBombQty', 'progressionDifficulty', 'progressionDifficultyMultiSelect', 'escapeRando', 'removeEscapeEnemies', 'funCombat', 'funMovement', 'funSuits', 'hideItems', 'strictMinors']:
            if param in paramsSet:
                paramsHead.append(param)
                paramsSet.remove(param)

        header = ["id", "actionTime", "guid", "returnCode", "duration", "errorMsg"]
        return (header, outData, paramsHead + sorted(list(paramsSet)))

    def getRandomizerParamsStats(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = """select rp.name, rp.value, count(*) as total
from randomizer_params rp
where rp.name not like '%%MultiSelect'
  and rp.name != 'seed'
  and rp.randomizer_id >= (select min(id) from randomizer where action_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK))
group by rp.name, rp.value
order by 1,2;"""

        rows = self.execSelect(sql, (weeks,))

        # transform it from [(param1, value1, count1), (param1, value2, count2), (param2, value3, count3)]
        # to [('parameter', 'value1', 'value2', value3', ...),
        #     (param1, count1, count2, 0, ...)
        #     (param2, 0, 0, count3, ...)]
        groups = {
            'Randomizer parameters': ['preset', 'startLocation', 'majorsSplit', 'scavNumLocs', 'scavRandomized', 'scavEscape', 'progressionSpeed', 'maxDifficulty', 'morphPlacement', 'progressionDifficulty', 'suitsRestriction', 'hideItems'],
            'Ammo and Energy': ['minorQty', 'energyQty', 'strictMinors', 'missileQty', 'superQty', 'powerBombQty'],
            'Areas and Fun': ['areaRandomization', 'lightAreaRandomization', 'areaLayout', 'doorsColorsRando', 'allowGreyDoors', 'bossRandomization', 'minimizer', 'minimizerQty', 'minimizerTourian', 'escapeRando', 'removeEscapeEnemies', 'funCombat', 'funMovement', 'funSuits'],
            'Patches': ['layoutPatches', 'variaTweaks', 'nerfedCharge', 'gravityBehaviour', 'itemsounds', 'elevators_doors_speed', 'spinjumprestart', 'rando_speed', 'Infinite_Space_Jump', 'refill_before_save', 'hud', 'animals', 'No_Music', 'random_music']
        }

        result = {}
        valuesIndex = {'Randomizer parameters': {}, 'Ammo and Energy': {}, 'Areas and Fun': {}, 'Patches': {}}
        paramsIndex = {'Randomizer parameters': {}, 'Ammo and Energy': {}, 'Areas and Fun': {}, 'Patches': {}}
        maxValuesIndex = {'Randomizer parameters': 1, 'Ammo and Energy': 1, 'Areas and Fun': 1, 'Patches': 1}
        firstRow = {'Randomizer parameters': ['parameter'], 'Ammo and Energy': ['parameter'], 'Areas and Fun': ['parameter'], 'Patches': ['parameter']}

        for group in groups.keys():
            for row in rows:
                param, value, count = row
                if param not in groups[group]:
                    continue
                if param not in paramsIndex[group]:
                    paramsIndex[group][param] = groups[group].index(param)+1
                if value not in valuesIndex[group]:
                    valuesIndex[group][value] = maxValuesIndex[group]
                    maxValuesIndex[group] += 1
                    firstRow[group].append(value)

            result[group] = [[0]*(maxValuesIndex[group]) for i in range(len(groups[group])+1)]
            result[group][0] = firstRow[group]
            for row in rows:
                param, value, count = row
                if param not in groups[group]:
                    continue
                paramIndex = paramsIndex[group][param]
                result[group][paramIndex][valuesIndex[group][value]] = count
                result[group][paramIndex][0] = param

        return result

    def getRandomizerSeedParamsAPI(self, guid):
        if self.dbAvailable == False:
            return None

        sql = "select rp.name, rp.value from randomizer_params rp join randomizer r on rp.randomizer_id = r.id where r.guid = '%s' order by rp.name;"
        data = self.execSelect(sql, (guid,))
        if data == None:
            return ""
        else:
            ret = "{"
            tmp = []
            for row in data:
                arg = row[0]
                value = row[1]
                if arg.find("MultiSelect") != -1:
                    value = '["{}"]'.format('", "'.join(value.split(',')))
                else:
                    value = '"{}"'.format(value)
                tmp.append('"{}": {}'.format(arg, value))
            ret += ','.join(tmp)
            ret += "}"
            return ret

    def getRandomizerSeedParams(self, randomizer_id):
        if self.dbAvailable == False:
            return None

        seed = 0
        sql = "select name, value from randomizer_params where randomizer_id = %d order by name;"
        data = self.execSelect(sql, (randomizer_id,))
        if data == None:
            return ""
        else:
            ret = "{\n"
            tmp = []
            for row in data:
                arg = row[0]
                value = row[1]
                if arg == 'seed':
                    seed = value
                if arg.find("MultiSelect") != -1:
                    value = '["{}"]'.format('", "'.join(value.split(',')))
                else:
                    value = '"{}"'.format(value)
                tmp.append('"{}": {}'.format(arg, value))
            ret += ',\n'.join(tmp)
            ret += "\n}"
            return (seed, ret)

    def getGeneratedSeeds(self, preset):
        if self.dbAvailable == False:
            return None

        sql = "select count(*) from randomizer_params where name = 'preset' and value = '%s';"
        data = self.execSelect(sql, (preset,))
        if data == None:
            return 0
        else:
            return data[0][0]

    def getPresetLastActionDate(self, preset):
        if self.dbAvailable == False:
            return None

        sql = "select max(action_time) from preset_action where preset = '%s';"
        data = self.execSelect(sql, (preset,))
        if data == None:
            return 'N/A'
        data = data[0][0] if data[0][0] != None else 'N/A'
        return data

        return self.execSelect(sql % (id,))

    def getSeedInfo(self, key):
        # key is id from randomizer table
        if self.dbAvailable == False:
            return None

        sql = """
select 'upload_status', upload_status
from randomizer
where guid = '%s'
union all
select 'filename', filename
from randomizer
where guid = '%s'
union all
select 'time', action_time
from randomizer
where guid = '%s'
union all
select name, value
from randomizer_params
where randomizer_id = (select id from randomizer where guid = '%s')
order by 1;"""

        return self.execSelect(sql % (key, key, key, key))

    def getSeedIpsInfo(self, key):
        # key is id from randomizer table
        if self.dbAvailable == False:
            return None

        sql = """select upload_status, filename from randomizer where guid = '%s';"""

        return self.execSelect(sql % (key,))

    def updateSeedUploadStatus(self, key, newStatus):
        # key is id from randomizer table
        if self.dbAvailable == False:
            return None

        try:
            sql = """update randomizer set upload_status = '%s' where guid = '%s';"""
            self.cursor.execute(sql % (newStatus, key))
        except Exception as e:
            print("DB.updateSeedUploadStatus::error execute: {}".format(e))
            self.dbAvailable = False

    def getISolver(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select distinct(preset) from isolver where init_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK);"
        presets = self.execSelect(sql, (weeks,))
        if presets == None:
            return None

        # db returns tuples
        presets = [preset[0] for preset in presets]

        # pivot
        sql = "SELECT date(init_time)"
        for preset in presets:
            sql += ", SUM(CASE WHEN preset = '{}' THEN 1 ELSE 0 END) AS count_{}".format(preset, preset)
        sql += " FROM isolver where init_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(init_time);".format(weeks)

        return (presets, self.execSelect(sql))

    def getISolverData(self, weeks):
        if self.dbAvailable == False:
            return None

        # return all data csv style
        sql = """select 0, init_time, type, preset, romFileName
from isolver
where init_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK)
order by init_time;"""

        header = ["initTime", "type", "preset", "romFileName"]
        return (header, self.execSelect(sql, (weeks,)))

    def getSpritesData(self, weeks):
        if self.dbAvailable == False:
            return None

        sql = "select distinct(sprite) from sprites where init_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK);"
        sprites = self.execSelect(sql, (weeks,))
        if sprites == None:
            return None

        # db returns tuples
        sprites = [sprite[0] for sprite in sprites]

        # pivot
        sql = "SELECT date(init_time)"
        for sprite in sprites:
            sql += ", SUM(CASE WHEN sprite = '{}' THEN 1 ELSE 0 END) AS count_{}".format(sprite, sprite.replace('-', '_'))
        sql += " FROM sprites where init_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(init_time);".format(weeks)

        return (sprites, self.execSelect(sql))

    def getPlandoRandoData(self, weeks):
        if self.dbAvailable == False:
            return None

        # return all data csv style
        sql = """select 0, init_time, return_code, duration, error_msg
from plando_rando
where init_time > DATE_SUB(CURDATE(), INTERVAL %d WEEK)
order by init_time;"""

        header = ["initTime", "returnCode", "duration", "errorMsg"]
        return (header, self.execSelect(sql, (weeks,)))

    @staticmethod
    def dumpItemLocs(locsItems, sqlFile):
        for (location, item) in locsItems.items():
            if item == 'Boss':
                continue
            # we can't have special chars in columns names
            location = removeChars(location, " ,()-")
            sql = "insert into item_locs (ext_id, item, {}) values (@last_id, '%s', 1) on duplicate key update {} = {} + 1;\n".format(location, location, location)

            sqlFile.write(sql % (item,))

    @staticmethod
    def dumpExtStatsItems(skillPreset, randoPreset, locsItems, sqlFile):
        sql = """insert into extended_stats (skillPreset, randoPreset, count)
values
('%s', '%s', 1)
on duplicate key update id=LAST_INSERT_ID(id), count = count + 1;
set @last_id = last_insert_id();
"""

        sqlFile.write(sql % (skillPreset, randoPreset))

        DB.dumpItemLocs(locsItems, sqlFile)

    @staticmethod
    def dumpExtStatsSolver(difficulty, techniques, solverStats, locsItems, step, sqlFile):
        # use @last_id defined by the randomizer

        if step == 1:
            DB.dumpItemLocs(locsItems, sqlFile)

            # get difficulty column
            if difficulty < medium:
                column = "easy"
            elif difficulty < hard:
                column = "medium"
            elif difficulty < harder:
                column = "hard"
            elif difficulty < hardcore:
                column = "harder"
            elif difficulty < mania:
                column = "hardcore"
            else:
                column = "mania"

            sql = "insert into difficulties (ext_id, {}) values (@last_id, 1) on duplicate key update {} = {} + 1;\n".format(column, column, column)
            sqlFile.write(sql)

            for technique in techniques:
                sql = "insert into techniques (ext_id, technique, count) values (@last_id, '%s', 1) on duplicate key update count = count + 1;\n"
                sqlFile.write(sql % (technique,))
        else:
            for (stat, value) in solverStats.items():
                sql = "insert into solver_stats (ext_id, name, value) values (@last_id, '%s', %d);\n"
                sqlFile.write(sql % (stat, value))

            # to avoid // issues
            sqlFile.write("commit;\n")

    def getExtStat(self, skillPreset, randoPreset):
        if self.dbAvailable == False:
            return (None, None, None, None)

        sqlItems = """select sum(e.count), i.item, round(100*sum(i.EnergyTankGauntlet)/sum(e.count), 1), round(100*sum(i.Bomb)/sum(e.count), 1), round(100*sum(i.EnergyTankTerminator)/sum(e.count), 1), round(100*sum(i.ReserveTankBrinstar)/sum(e.count), 1), round(100*sum(i.ChargeBeam)/sum(e.count), 1), round(100*sum(i.MorphingBall)/sum(e.count), 1), round(100*sum(i.EnergyTankBrinstarCeiling)/sum(e.count), 1), round(100*sum(i.EnergyTankEtecoons)/sum(e.count), 1), round(100*sum(i.EnergyTankWaterway)/sum(e.count), 1), round(100*sum(i.EnergyTankBrinstarGate)/sum(e.count), 1), round(100*sum(i.XRayScope)/sum(e.count), 1), round(100*sum(i.Spazer)/sum(e.count), 1), round(100*sum(i.EnergyTankKraid)/sum(e.count), 1), round(100*sum(i.Kraid)/sum(e.count), 1), round(100*sum(i.VariaSuit)/sum(e.count), 1), round(100*sum(i.IceBeam)/sum(e.count), 1), round(100*sum(i.EnergyTankCrocomire)/sum(e.count), 1), round(100*sum(i.HiJumpBoots)/sum(e.count), 1), round(100*sum(i.GrappleBeam)/sum(e.count), 1), round(100*sum(i.ReserveTankNorfair)/sum(e.count), 1), round(100*sum(i.SpeedBooster)/sum(e.count), 1), round(100*sum(i.WaveBeam)/sum(e.count), 1), round(100*sum(i.Ridley)/sum(e.count), 1), round(100*sum(i.EnergyTankRidley)/sum(e.count), 1), round(100*sum(i.ScrewAttack)/sum(e.count), 1), round(100*sum(i.EnergyTankFirefleas)/sum(e.count), 1), round(100*sum(i.ReserveTankWreckedShip)/sum(e.count), 1), round(100*sum(i.EnergyTankWreckedShip)/sum(e.count), 1), round(100*sum(i.Phantoon)/sum(e.count), 1), round(100*sum(i.RightSuperWreckedShip)/sum(e.count), 1), round(100*sum(i.GravitySuit)/sum(e.count), 1), round(100*sum(i.EnergyTankMamaturtle)/sum(e.count), 1), round(100*sum(i.PlasmaBeam)/sum(e.count), 1), round(100*sum(i.ReserveTankMaridia)/sum(e.count), 1), round(100*sum(i.SpringBall)/sum(e.count), 1), round(100*sum(i.EnergyTankBotwoon)/sum(e.count), 1), round(100*sum(i.Draygon)/sum(e.count), 1), round(100*sum(i.SpaceJump)/sum(e.count), 1), round(100*sum(i.MotherBrain)/sum(e.count), 1), round(100*sum(i.PowerBombCrateriasurface)/sum(e.count), 1), round(100*sum(i.MissileoutsideWreckedShipbottom)/sum(e.count), 1), round(100*sum(i.MissileoutsideWreckedShiptop)/sum(e.count), 1), round(100*sum(i.MissileoutsideWreckedShipmiddle)/sum(e.count), 1), round(100*sum(i.MissileCrateriamoat)/sum(e.count), 1), round(100*sum(i.MissileCrateriabottom)/sum(e.count), 1), round(100*sum(i.MissileCrateriagauntletright)/sum(e.count), 1), round(100*sum(i.MissileCrateriagauntletleft)/sum(e.count), 1), round(100*sum(i.SuperMissileCrateria)/sum(e.count), 1), round(100*sum(i.MissileCrateriamiddle)/sum(e.count), 1), round(100*sum(i.PowerBombgreenBrinstarbottom)/sum(e.count), 1), round(100*sum(i.SuperMissilepinkBrinstar)/sum(e.count), 1), round(100*sum(i.MissilegreenBrinstarbelowsupermissile)/sum(e.count), 1), round(100*sum(i.SuperMissilegreenBrinstartop)/sum(e.count), 1), round(100*sum(i.MissilegreenBrinstarbehindmissile)/sum(e.count), 1), round(100*sum(i.MissilegreenBrinstarbehindreservetank)/sum(e.count), 1), round(100*sum(i.MissilepinkBrinstartop)/sum(e.count), 1), round(100*sum(i.MissilepinkBrinstarbottom)/sum(e.count), 1), round(100*sum(i.PowerBombpinkBrinstar)/sum(e.count), 1), round(100*sum(i.MissilegreenBrinstarpipe)/sum(e.count), 1), round(100*sum(i.PowerBombblueBrinstar)/sum(e.count), 1), round(100*sum(i.MissileblueBrinstarmiddle)/sum(e.count), 1), round(100*sum(i.SuperMissilegreenBrinstarbottom)/sum(e.count), 1), round(100*sum(i.MissileblueBrinstarbottom)/sum(e.count), 1), round(100*sum(i.MissileblueBrinstartop)/sum(e.count), 1), round(100*sum(i.MissileblueBrinstarbehindmissile)/sum(e.count), 1), round(100*sum(i.PowerBombredBrinstarsidehopperroom)/sum(e.count), 1), round(100*sum(i.PowerBombredBrinstarspikeroom)/sum(e.count), 1), round(100*sum(i.MissileredBrinstarspikeroom)/sum(e.count), 1), round(100*sum(i.MissileKraid)/sum(e.count), 1), round(100*sum(i.Missilelavaroom)/sum(e.count), 1), round(100*sum(i.MissilebelowIceBeam)/sum(e.count), 1), round(100*sum(i.MissileaboveCrocomire)/sum(e.count), 1), round(100*sum(i.MissileHiJumpBoots)/sum(e.count), 1), round(100*sum(i.EnergyTankHiJumpBoots)/sum(e.count), 1), round(100*sum(i.PowerBombCrocomire)/sum(e.count), 1), round(100*sum(i.MissilebelowCrocomire)/sum(e.count), 1), round(100*sum(i.MissileGrappleBeam)/sum(e.count), 1), round(100*sum(i.MissileNorfairReserveTank)/sum(e.count), 1), round(100*sum(i.MissilebubbleNorfairgreendoor)/sum(e.count), 1), round(100*sum(i.MissilebubbleNorfair)/sum(e.count), 1), round(100*sum(i.MissileSpeedBooster)/sum(e.count), 1), round(100*sum(i.MissileWaveBeam)/sum(e.count), 1), round(100*sum(i.MissileGoldTorizo)/sum(e.count), 1), round(100*sum(i.SuperMissileGoldTorizo)/sum(e.count), 1), round(100*sum(i.MissileMickeyMouseroom)/sum(e.count), 1), round(100*sum(i.MissilelowerNorfairabovefireflearoom)/sum(e.count), 1), round(100*sum(i.PowerBomblowerNorfairabovefireflearoom)/sum(e.count), 1), round(100*sum(i.PowerBombPowerBombsofshame)/sum(e.count), 1), round(100*sum(i.MissilelowerNorfairnearWaveBeam)/sum(e.count), 1), round(100*sum(i.MissileWreckedShipmiddle)/sum(e.count), 1), round(100*sum(i.MissileGravitySuit)/sum(e.count), 1), round(100*sum(i.MissileWreckedShiptop)/sum(e.count), 1), round(100*sum(i.SuperMissileWreckedShipleft)/sum(e.count), 1), round(100*sum(i.MissilegreenMaridiashinespark)/sum(e.count), 1), round(100*sum(i.SuperMissilegreenMaridia)/sum(e.count), 1), round(100*sum(i.MissilegreenMaridiatatori)/sum(e.count), 1), round(100*sum(i.SuperMissileyellowMaridia)/sum(e.count), 1), round(100*sum(i.MissileyellowMaridiasupermissile)/sum(e.count), 1), round(100*sum(i.MissileyellowMaridiafalsewall)/sum(e.count), 1), round(100*sum(i.MissileleftMaridiasandpitroom)/sum(e.count), 1), round(100*sum(i.MissilerightMaridiasandpitroom)/sum(e.count), 1), round(100*sum(i.PowerBombrightMaridiasandpitroom)/sum(e.count), 1), round(100*sum(i.MissilepinkMaridia)/sum(e.count), 1), round(100*sum(i.SuperMissilepinkMaridia)/sum(e.count), 1), round(100*sum(i.MissileDraygon)/sum(e.count), 1)
from extended_stats e join item_locs i on e.id = i.ext_id
where item not in ('Nothing', 'NoEnergy', 'ETank', 'Reserve', 'Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain')
  and e.skillPreset = '%s' and e.randoPreset = '%s'
group by i.item
order by i.item;"""

        sqlTechniques = """select t.technique, round(100*sum(t.count)/sum(e.count), 1)
from extended_stats e
  join techniques t on e.id = t.ext_id
where e.skillPreset = '%s' and e.randoPreset = '%s'
group by t.technique;"""

        sqlDifficulties = """
select sum(d.easy), sum(d.medium), sum(d.hard), sum(d.harder), sum(d.hardcore), sum(d.mania)
from extended_stats e
  join difficulties d on e.id = d.ext_id
where e.skillPreset = '%s' and e.randoPreset = '%s';"""

        sqlSolverStats = """
select s.name, s.value, round(count(*) * 100 / e.count, 1)
from extended_stats e
  join solver_stats s on e.id = s.ext_id
where e.skillPreset = '%s' and e.randoPreset = '%s'
group by s.name, s.value
order by 1,2;"""

        items = self.execSelect(sqlItems, (skillPreset, randoPreset))

        techniques = self.execSelect(sqlTechniques, (skillPreset, randoPreset))
        # transform techniques into a dict
        techOut = {}
        if techniques != None:
            for technique in techniques:
                techOut[technique[0]] = technique[1]

        difficulties = self.execSelect(sqlDifficulties, (skillPreset, randoPreset))
        if difficulties != None:
            difficulties = difficulties[0]

            # check if all values are null
            if difficulties.count(None) == len(difficulties):
                difficulties = []

        solverStats = self.execSelect(sqlSolverStats, (skillPreset, randoPreset))
        solverStatsOut = {}
        if solverStats != None:
            for stat in solverStats:
                (name, value, count) = stat
                if name not in solverStatsOut:
                    solverStatsOut[name] = []
                solverStatsOut[name].append((value, count))

        return (items, techOut, difficulties, solverStatsOut)

    def getProgSpeedStat(self, skillPreset, randoPreset):
        if self.dbAvailable == False:
            return None

        sqlSolverStats = """
select s.name, s.value, round(count(*) * 100 / e.count, 1)
from extended_stats e
  join solver_stats s on e.id = s.ext_id
where e.skillPreset = '%s' and e.randoPreset = '%s'
group by s.name, s.value
order by 1,2;"""

        solverStats = self.execSelect(sqlSolverStats, (skillPreset, randoPreset))
        solverStatsOut = {}
        if solverStats != None:
            for stat in solverStats:
                (name, value, count) = stat
                if name not in solverStatsOut:
                    solverStatsOut[name] = []
                solverStatsOut[name].append((value, count))

        return solverStatsOut

    def getPlandos(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select re.plando_name, re.init_time, re.author, re.long_desc, re.suggested_preset, re.download_count, (select sum(ra.rating)/count(1) from plando_rating ra where ra.plando_name = re.plando_name), (select count(1) from plando_rating ra where ra.plando_name = re.plando_name) from plando_repo re;"
            return self.execSelect(sql)
        except Exception as e:
            print("DB.getPlandos::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def getPlando(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select re.plando_name, re.init_time, re.author, re.long_desc, re.suggested_preset, re.download_count, (select sum(ra.rating)/count(1) from plando_rating ra where ra.plando_name = re.plando_name), (select count(1) from plando_rating ra where ra.plando_name = re.plando_name) from plando_repo re where re.plando_name = '%s';"
            return self.execSelect(sql, (plandoName,))
        except Exception as e:
            print("DB.getPlando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def getPlandoCount(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select count(1) from plando_repo;"
            return self.execSelect(sql)
        except Exception as e:
            print("DB.getPlandoCount::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def checkPlando(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select plando_name from plando_repo where plando_name = '%s';"
            return self.execSelect(sql, (plandoName,))
        except Exception as e:
            print("DB.checkPlando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def getPlandoIpsMaxSize(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select ips_max_size from plando_repo where plando_name = '%s';"
            return self.execSelect(sql, (plandoName,))
        except Exception as e:
            print("DB.getPlandoIpsMaxSize::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def getPlandoRate(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select count(1), sum(rating)/count(1) from plando_rating where plando_name = '%s';"
            return self.execSelect(sql, (plandoName,))
        except Exception as e:
            print("DB.getPlandoRate::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def insertPlando(self, params):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into plando_repo (plando_name, init_time, author, long_desc, suggested_preset, update_key, ips_max_size) values ('%s', now(), '%s', '%s', '%s', '%s', %d);"
            self.cursor.execute(sql % params)
            self.commit()
        except Exception as e:
            print("DB.insertPlando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def updatePlandoAll(self, params):
        if self.dbAvailable == False:
            return None

        try:
            sql = "update plando_repo set init_time = now(), author = '%s', long_desc = '%s', suggested_preset = '%s', ips_max_size = %d where plando_name = '%s'"
            self.cursor.execute(sql % params)
            self.commit()
        except Exception as e:
            print("DB.updatePlandoAll::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def updatePlandoMeta(self, params):
        if self.dbAvailable == False:
            return None

        try:
            sql = "update plando_repo set author = '%s', long_desc = '%s', suggested_preset = '%s' where plando_name = '%s'"
            self.cursor.execute(sql % params)
            self.commit()
        except Exception as e:
            print("DB.updatePlandoMeta::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def alreadyRated(self, plandoName, ip):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select 1 from plando_rating where plando_name = '%s' and ipv4 = inet_aton('%s');"
            return self.execSelect(sql % (plandoName, ip))
        except Exception as e:
            print("DB.alreadyRated::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addRating(self, plandoName, rating, ip):
        if self.dbAvailable == False:
            return None

        try:
            sql = """
REPLACE INTO plando_rating
    (plando_name, rating, ipv4)
VALUES ('%s', %d, inet_aton('%s'));"""
            self.cursor.execute(sql % (plandoName, rating, ip))
            self.commit()
        except Exception as e:
            print("DB.addRating::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def increaseDownloadCount(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "update plando_repo set download_count = download_count+1 where plando_name = '%s';"
            self.cursor.execute(sql % (plandoName,))
            self.commit()
        except Exception as e:
            print("DB.increaseDownloadCount::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def isValidPlandoKey(self, plandoName, key):
        if self.dbAvailable == False:
            return None

        try:
            sql = "select 1 from plando_repo where plando_name = '%s' and update_key = '%s';"
            return self.execSelect(sql % (plandoName, key))
        except Exception as e:
            print("DB.isValidPlandoKey::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def deletePlando(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "delete from plando_repo where plando_name = '%s';"
            self.cursor.execute(sql % (plandoName,))
            self.commit()
        except Exception as e:
            print("DB.deletePlando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def deletePlandoRating(self, plandoName):
        if self.dbAvailable == False:
            return None

        try:
            sql = "delete from plando_rating where plando_name = '%s';"
            self.cursor.execute(sql % (plandoName,))
            self.commit()
        except Exception as e:
            print("DB.deletePlandoRating::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False
