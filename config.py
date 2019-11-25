from pymysql.cursors import DictCursor

database = {
	"host"			:'127.0.0.1',
	"user"			:'root',
	"password"		:'password',
	"db"			: 'matcha',
	"charset"		: 'utf8mb4',
	"cursorclass"	: DictCursor
}