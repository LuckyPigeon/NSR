/*
  資料表:
	Class: 紀錄目錄架構的成員，在此為由首頁、小說種類、作者、小說名稱等四種類型成員組成的資料表
	Information: Class 的擴充欄位（繼承），紀錄小說的書籍基本資訊
	Object: 紀錄小說的章回名稱
	Paragraph: 紀錄小說的段落內容
	Sentence: 紀錄小說的句子內容
	Segment: 紀錄小說的句子片段內容
	Token: 紀錄小說所有詞彙
	Keyword: 繼承自Token，紀錄小說所有有特殊意義之詞彙
	Works: 紀錄由小說發展出的改編作品、電玩遊戲以及周邊商品
  關聯資料表:
    CRel: 紀錄 Class 成員之間的父子關係（目錄關係）
	CO: 紀錄小說與其章回名稱的關聯
	OP: 紀錄小說章回名稱與段落內容的關聯
	PS: 紀錄小說段落內容與句子內容的關聯
	SS: 紀錄小說句子內容與句子片段內容的關聯
	ST: 紀錄小說句子片段內容與所有詞彙的關聯
	CI: 紀錄小說名稱與書籍基本資訊的關聯
	CW: 紀錄小說名稱與改編作品、電玩遊戲以及周邊商品的關係
    
*/

CREATE TABLE CRel (
    ParentID INT NOT NULL,
    ChildID INT NOT NULL,
	Rank INT NOT NULL,
    PRIMARY KEY(ParentID, ChildID, Rank)
)

CREATE TABLE Class (
    id INT NOT NULL PRIMARY KEY,
	idpath VARCHAR(32),
    name VARCHAR(64) NOT NULL,
	namepath VARCHAR(256),
	author VARCHAR(32) NOT NULL,
	location VARCHAR(64) NOT NULL,
	lang VARCHAR(16) NOT NULL DEFAULT '中文',
	category VARCHAR(16) NOT NULL DEFAULT '武俠',
	type VARCHAR(16) NOT NULL DEFAULT '小說',
	publisher VARCHAR(32) NOT NULL,
	pubDate DATE NOT NULL,
	pubDateZh DATE NOT NULL,
	format VARCHAR(16) NOT NULL DEFAULT '紙本',
	pages SMALLINT NOT NULL,
	lastbook VARCHAR(64),
	nextbook VARCHAR(64),
	url VARCHAR(512),
	description VARCHAR,
	isActive BOOLEAN,
	isDel BOOLEAN,
	level BIT(8) NOT NULL
)

CREATE TABLE Information (
	id INT NOT NULL,
	background VARCHAR,
	v_name VARCHAR(64), -- version name
	v_date DATE, -- version date
	v_des VARCHAR, -- version description
	evalutate VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES Class(id)
)
