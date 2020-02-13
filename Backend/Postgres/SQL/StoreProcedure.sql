/*
  Store Procedure:
	sp_insertClass: 將資訊插入 Class 資料表，並在 CRel 中建立關聯
    sp_insertInformation: 將小說的基本資訊插入 Information 資料表
    sp_createPath: 建立 Class 資料表的 namepath & idpath
    sp_insertChapter: 將章回名稱插入 Object 資料表，並在 Chapter 資料表中建立其資訊，接著建立 CO 關聯
    sp_insertParagraph: 將段落插入 Paragraph 資料表，並在 OP 中建立關聯
    sp_insertSentence: 將句子插入 Sentence 資料表，並在 SP 中建立關聯
    sp_insertSegment: 將句子片段插入 Segment 資料表，並在 SS 中建立關聯
    sp_insertToken: 將詞彙插入 Token 資料表，並在 ST 中建立關聯
    sp_insertKeyword: 將詞彙插入 Keyword 資料表
    sp_insertPatternword: 將重複出現詞彙插入 Patternword 資料表
    sp_insertWorks: 將改編作品、電玩遊戲以及周邊商品資訊插入 Object 資料表，並在 Chapter 資料表中建立其資訊，接著建立 CO 關聯
*/