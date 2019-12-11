import sqlite3
from contextlib import closing

def insertMaster(key, value):
	# masterにデータを追加する
	def getHistory(c, key, value):
		# 履歴最大値取得
		sql = '''
			select 
				case 
					when max(history) is NULL then 0 else max(history) + 1 
				end
			from master
			where key = ?
			and value <> ?
		'''
		history = c.execute(sql, [key, value]).fetchone()[0]

		return history

	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()

		# 履歴最大値取得
		history = getHistory(c, key, value)
		# データ作成 & 更新
		sql = '''
			insert or replace into master (key, value, history) 
			values (?, ?, ?)
		'''
		data = (key, value, history)
		c.execute(sql, data)
		conn.commit()
	
	# そのうちきれいにしたいね
	updateMasterHistory(key)

def selectMaster(key):
	# 指定されたkeyのvalueリストを取得する
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()

		sql = '''
			select value
			from master
			where key = ?
			order by history desc
		'''

		valueList = []
		reader = c.execute(sql, [key])
		for row in reader:
			valueList.append(row[0])
	
	return valueList

def deleteMaster(key, value):
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		# データ削除
		sql = '''
			delete from
				master
			where 
				key = ?
				and value = ?
		'''
		data = (key, value)
		c.execute(sql, data)
		conn.commit()

def insertBattle(battle_id, key, value):
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		# データ作成 & 更新
		sql = '''
			insert or replace into battle (battle_id, key, value) 
			values (?, ?, ?)
		'''
		data = (battle_id, key, value)
		c.execute(sql, data)
		conn.commit()

def insertResult(battle_id, match_id, key, value):
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		# データ作成 & 更新
		sql = '''
			insert or replace into result (battle_id, match_id, key, value) 
			values (?, ?, ?, ?)
		'''
		data = (battle_id, match_id, key, value)
		c.execute(sql, data)
		conn.commit()

def createScore():
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		
		id = getMaxIdAddOne(c, 'battle', 'battle_id')
		insertBattle(id, 'entry_count', '1')
	return id

def deleteScore(battle_id):
	dbName = 'tScore' + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		# データ作成 & 更新
		deleteBattleSql = '''
			delete from battle
			where battle_id = ?
		'''
		deleteResultSql = '''
			delete from result
			where battle_id = ?
		'''
		data = (battle_id, )
		c.execute(deleteBattleSql, data)
		c.execute(deleteResultSql, data)
		conn.commit()

def updateMasterHistory(*_):
	# ToDo
	# masterのhistoryに穴が開くから整理したい
	pass

def getMaxIdAddOne(c, table, col):
	# 履歴最大値取得
	sql = 'select case when max(' + col + ') is NULL then 0 else max(' + col + ') + 1 end from ' + table
	maxId = c.execute(sql).fetchone()[0]

	return maxId

def main():
	# データ入力
	# 新規 or 編集
	battleId = createScore()
	# battleId = '0'
	# 大会全体について
	key = 'tcg_type'
	value = 'Doreno'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'battle_name'
	value = '公認大会'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'battle_place'
	value = '火星TSUYATA'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'battle_date'
	value = '2025-01-05'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'battle_format'
	value = 'スタンダード'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'player_deck'
	value = '青青アテナ'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'entry_count'
	value = '14'
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	key = 'memo'
	value = ''
	insertMaster(key, value)
	insertBattle(battleId, key, value)
	# マッチについて
	# 1回戦
	matchId = '1'
	key = 'opponent_name'
	value = 'morisoba'
	insertResult(battleId, matchId, key, value)
	key = 'opponent_deck'
	value = '青黒ゴモリー'
	insertResult(battleId, matchId, key, value)
	key = 'is_first'
	value = 'T'
	insertResult(battleId, matchId, key, value)
	key = 'result'
	value = 'win'
	insertResult(battleId, matchId, key, value)
	key = 'memo'
	value = 'ジャッチキル'
	insertResult(battleId, matchId, key, value)
	# 2回戦
	matchId = '2'
	key = 'opponent_name'
	value = 'さんじょ'
	insertResult(battleId, matchId, key, value)
	key = 'opponent_deck'
	value = '青青アテナ'
	insertResult(battleId, matchId, key, value)
	key = 'is_first'
	value = 'T'
	insertResult(battleId, matchId, key, value)
	key = 'result'
	value = 'lose'
	insertResult(battleId, matchId, key, value)
	key = 'memo'
	value = 'アウグル出さないことによる引き分け'
	insertResult(battleId, matchId, key, value)
	# 3回戦
	matchId = '3'
	key = 'opponent_name'
	value = 'ぼーかる'
	insertResult(battleId, matchId, key, value)
	key = 'opponent_deck'
	value = '青黒ゴモリー'
	insertResult(battleId, matchId, key, value)
	key = 'is_first'
	value = 'T'
	insertResult(battleId, matchId, key, value)
	key = 'result'
	value = 'win'
	insertResult(battleId, matchId, key, value)
	key = 'memo'
	value = 'わかる'
	insertResult(battleId, matchId, key, value)

	# deleteScore('0')
	# deleteMaster(key, value)

if __name__ == '__main__':
	main()

# めもるやつ２
# battle_id 大会ID(自動)
# match_id マッチID(回戦数)
# player_deck 自デッキ(変更自由かも知れない)
# opponent_name 相手名前
# opponent_deck 相手デッキ
# result 成績(勝ち負け引き分けのみ。自由入力させない)
# memo めも