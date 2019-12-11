import sqlite3
from contextlib import closing

# memo
# NULL       NULL値
# INTEGER    符号付整数。1, 2, 3, 4, 6, or 8 バイトで格納
# REAL       浮動小数点数。8バイトで格納
# TEXT       テキスト。UTF-8, UTF-16BE or UTF-16-LEのいずれかで格納
# BLOB       Binary Large OBject。入力データをそのまま格納

# 管理するやつ(選択肢化させたいやつ)
# tcg_type 種類
# place 場所(店舗)
# format フォーマット
# player_deck 自デッキ
# opponent_name 相名前
# opponent_deck 相デッキ

# めもるやつ１
# battle_id 大会ID(自動)
# tcg_type TCG種類
# battle_name 大会名(ツタヤ公認とか)
# battle_place 大会場所(火星ツタヤとか)
# battle_date 大会日(2900/1/1)
# battle_format 大会フォーマット(スタンダード)
# player_deck 自デッキ(変更自由かも知れない)
# entry_count 参加人数
# memo めも

# めもるやつ２
# battle_id 大会ID(自動)
# match_id マッチID(回戦数)
# opponent_name 相手名前
# opponent_deck 相手デッキ
# result 成績(勝ち負け引き分けのみ。自由入力させない)
# memo めも

def createDataBase(dbName):
	dbName = dbName + '.sqlite3'
	with closing(sqlite3.connect(dbName)) as conn:
		c = conn.cursor()
		# executeメソッドでSQL文を実行する
		create_table = '''
			create table master (
				key TEXT NOT NULL
				, value TEXT
				, history INTEGER
				, PRIMARY KEY (key, value)
			);
		'''
		c.execute(create_table)

		create_table = '''
			create table battle (
				battle_id INTEGER NOT NULL
				, key TEXT
				, value TEXT
 				, PRIMARY KEY(battle_id, key)
			);
		'''
		c.execute(create_table)

		create_table = '''
			create table result (
				battle_id INTEGER NOT NULL
				, match_id INTEGER NOT NULL
				, key TEXT
				, value TEXT
				, PRIMARY KEY(battle_id, match_id, key)
			);
		'''
		c.execute(create_table)

		create_table = '''
			create view battle_info AS 
				select
					base.battle_id battle_id
					, type.value battle_type
					, name.value battle_name
					, place.value battle_place
					, date.value battle_date
					, format.value battle_format
					, deck.value battle_deck
					, entry.value entry_count
					, memo.value battle_memo
				from 
					(
						select
							battle_id
						from 
							battle
						group by
							battle_id
					) base
					left join battle type
						on base.battle_id = type.battle_id
						and type.key = 'tcg_type'
					left join battle name
						on base.battle_id = name.battle_id
						and name.key = 'battle_name'
					left join battle place
						on base.battle_id = place.battle_id
						and place.key = 'battle_place'
					left join battle date
						on base.battle_id = date.battle_id
						and date.key = 'battle_date'
					left join battle deck
						on base.battle_id = deck.battle_id
						and deck.key = 'player_deck'
					left join battle format
						on base.battle_id = format.battle_id
						and format.key = 'battle_format'
					left join battle entry
						on base.battle_id = entry.battle_id
						and entry.key = 'entry_count'
					left join battle memo
						on base.battle_id = memo.battle_id
						and memo.key = 'memo'
			;
		'''
		c.execute(create_table)
		
		create_table = '''
			create view result_info AS 
			select 
				BASE.*
				, name.value name
				, deck.value deck
				, first.value is_first
				, winlose.value winlose
				, memo.value memo
			from (
				select battle_id, match_id
				from result
				group by battle_id, match_id
			) BASE
			left join result name
				on BASE.battle_id = name.battle_id
				and BASE.match_id = name.match_id
				and name.key = 'opponent_name'
			left join result deck
				on BASE.battle_id = deck.battle_id
				and BASE.match_id = deck.match_id
				and deck.key = 'opponent_deck'
			left join result first
				on BASE.battle_id = first.battle_id
				and BASE.match_id = first.match_id
				and first.key = 'is_first'
			left join result winlose
				on BASE.battle_id = winlose.battle_id
				and BASE.match_id = winlose.match_id
				and winlose.key = 'result'
			left join result memo
				on BASE.battle_id = memo.battle_id
				and BASE.match_id = memo.match_id
				and memo.key = 'memo'
			;
		'''
		c.execute(create_table)


		create_table = '''
			create view battle_score_info AS 
			select
				b.battle_id
				, b.battle_date
				, b.battle_type
				, b.battle_place
				, b.battle_format
				, b.battle_deck
				, case when w.win is null then '0' else w.win end win
				, case when l.lose is null then '0' else l.lose end lose
				, case when d.draw is null then '0' else d.draw end draw
			from
				battle_info b
				left join (
					select
						battle_id
						, count(*) win
					from
						result_info
					where
						winlose = 'win'
					group by
						battle_id
				) w
				on b.battle_id = w.battle_id
				left join (
					select
						battle_id
						, count(*) lose
					from
						result_info
					where
						winlose = 'lose'
					group by
						battle_id
				) l
				on b.battle_id = l.battle_id
				left join (
					select
						battle_id
						, count(*) draw
					from
						result_info
					where
						winlose = 'draw'
					group by
						battle_id
				) d
				on b.battle_id = d.battle_id
			order by
				b.battle_date desc
				, b.battle_id desc
			;
		'''
		c.execute(create_table)

def main():
	dbName = 'tScore'
	createDataBase(dbName)
	print('created!!')

if __name__ == '__main__':
	main()
