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
    ORel: 紀錄 Object 成員之間的關係
	CO: 紀錄小說與其章回名稱的關聯
	OP: 紀錄小說章回名稱與段落內容的關聯
	PS: 紀錄小說段落內容與句子內容的關聯
	SS: 紀錄小說句子內容與句子片段內容的關聯
	ST: 紀錄小說句子片段內容與所有詞彙的關聯
	CI: 紀錄小說名稱與書籍基本資訊的關聯
	CW: 紀錄小說名稱與改編作品、電玩遊戲以及周邊商品的關係
*/

--- 資料表 START ---
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
	id INT NOT NULL,
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
    id INT NOT NULL,
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
    id INT NOT NULL,
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
    PRIMARY KEY (id)
)

CREATE TABLE Sentence (
    id SERIAL NOT NULL,
    text VARCHAR NOT NULL,
    md5 BYTEA NOT NULL UNIQUE,
    total INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
)

CREATE TABLE Segment (
    id SERIAL NOT NULL,
    text VARCHAR(256) NOT NULL,
    total INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
)

CREATE TABLE Token (
    id SERIAL NOT NULL,
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

CREATE TABLE Patternword (
    id SERIAL NOT NULL,
    text VARCHAR(32) NOT NULL UNIQUE,
    type BIT(8),
    categoryid INT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (categoryid) REFERENCES Class(id)
)
--- 資料表 END ---

--- 關聯資料表 START ---
CREATE TABLE CRel (
    ParentID INT NOT NULL,
    ChildID INT NOT NULL,
	Rank INT NOT NULL,
    PRIMARY KEY (ParentID, ChildID, Rank),
    FOREIGN KEY (ParentID) REFERENCES Class(id),
    FOREIGN KEY (ChildID) REFERENCES Class(id)
)

CREATE TABLE ORel (
    id1 INT NOT NULL,
    id2 INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (id1, id2, Rank),
    FOREIGN KEY (id1) REFERENCES Object(id),
    FOREIGN KEY (id2) REFERENCES Object(id)
)

CREATE TABLE CO (
    CID INT NOT NULL,
    OID INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (CID, OID, Rank),
    FOREIGN KEY (CID) REFERENCES Class(id),
    FOREIGN KEY (OID) REFERENCES Object(id)
)

CREATE TABLE OP (
    id1 INT NOT NULL,
    id2 INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (id1, id2, Rank),
    FOREIGN KEY (id1) REFERENCES Object(id),
    FOREIGN KEY (id2) REFERENCES Paragraph(id)
)

CREATE TABLE PS (
    id1 INT NOT NULL,
    id2 INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (id1, id2, Rank),
    FOREIGN KEY (id1) REFERENCES Paragraph(id),
    FOREIGN KEY (id2) REFERENCES Sentence(id)
)

CREATE TABLE SS (
    id1 INT NOT NULL,
    id2 INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (id1, id2, Rank),
    FOREIGN KEY (id1) REFERENCES Sentence(id),
    FOREIGN KEY (id2) REFERENCES Segment(id)
)

CREATE TABLE ST (
    id1 INT NOT NULL,
    id2 INT NOT NULL,
    Rank INT NOT NULL,
    PRIMARY KEY (id1, id2, Rank),
    FOREIGN KEY (id1) REFERENCES Segment(id),
    FOREIGN KEY (id2) REFERENCES Token(id)
)
--- 關聯資料表 END ---
