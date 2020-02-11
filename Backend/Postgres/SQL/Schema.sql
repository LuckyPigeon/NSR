/*
  資料表:
	Class: 紀錄目錄架構的成員，在此為由首頁、小說種類、作者、小說名稱等四種類型成員組成的資料表
	Information: Class 的擴充欄位（繼承），紀錄小說的書籍基本資訊
	Object: 紀錄與小說關聯的物件資訊，包含 Chapter & Works
    Chapter: 繼承自 Object，紀錄小說的章回名稱
	Paragraph: 紀錄小說的段落內容
	Sentence: 紀錄小說的句子內容
	Segment: 紀錄小說的句子片段內容
	Token: 紀錄小說所有詞彙
	Keyword: 繼承自Token，紀錄小說所有有特殊意義之詞彙
    Patternword: 紀錄有意義且會重複出現的詞，如，姓氏
	Works: 繼承自 Object，紀錄由小說發展出的改編作品、電玩遊戲以及周邊商品
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

CREATE OR ALTER TABLE CRel (
    ParentID INT NOT NULL,
    ChildID INT NOT NULL,
	Rank INT NOT NULL,
    PRIMARY KEY(ParentID, ChildID, Rank)
)

CREATE TABLE Class (
    id SERIAL NOT NULL PRIMARY KEY,
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
    since DATE NOT NULL DEFAULT NOW(),
    limitDate DATE NOT NULL DEFAULT NOW(),
    delDate DATE NOT NULL DEFAULT NOW(),
	isActive BOOLEAN,
	isDel BOOLEAN,
	level BIT(8) NOT NULL
)

CREATE TABLE Information (
	id SERIAL NOT NULL,
	background VARCHAR,
	v_name VARCHAR(64), -- version name
	v_date DATE, -- version date
	v_des VARCHAR, -- version description
	evalutate VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES Class(id)
)

CREATE TABLE Object (
    id SERIAL NOT NULL,
    name VARCHAR(256),
    description VARCHAR,
    url VARCHAR(512),
    since DATE NOT NULL DEFAULT NOW(),
    lastModified DATE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Object(id)
)

CREATE TABLE Chapter (
    id SERIAL NOT NULL,
    name VARCHAR(256),
    description VARCHAR,
    url VARCHAR(512),
    status BIT(8),
    since DATE NOT NULL DEFAULT NOW(),
    lastModified DATE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Object(id)
)

CREATE TABLE Works (
    id SERIAL NOT NULL,
    name VARCHAR(256),
    description VARCHAR,
    url VARCHAR(512),
    type BIT(4),
    status BIT(8),
    since DATE NOT NULL DEFAULT NOW(),
    lastModified DATE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Object(id)
)

CREATE TABLE Paragraph (
    id SERIAL NOT NULL,
    text VARCHAR NOT NULL,
    md5 BYTEA NOT NULL UNIQUE,
    total INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
)

CREATE TABLE Sentence (
    id SERIAL NOT NULL,
    text VARCHAR NOT NULL,
    md5 BYTEA NOT NULL UNIQUE,
    total INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
)

CREATE TABLE Segment (
    id INT SERIAL NOT NULL,
    text VARCHAR(256) NOT NULL,
    total INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
)

CREATE TABLE Token (
    id INT SERIAL NOT NULL,
    text VARCHAR(64) NOT NULL,
    total INT NOT NULL DEFAULT 0,
    pos VARCHAR(4) NOT NULL,
    alias INT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (alias) REFERENCES Token(id)
)

CREATE TABLE Keyword (
    id INT NOT NULL,
    text VARCHAR(32) NOT NULL,
    total INT NOT NULL DEFAULT 0,
    pos VARCHAR(4) NOT NULL,
    type BIT(8),
    alias INT NULL,
    weight double precision,
    PRIMARY KEY (id),
    FOREIGN KEY (alias) REFERENCES Token(id),
    FOREIGN KEY (id) REFERENCES Token(id)
)
