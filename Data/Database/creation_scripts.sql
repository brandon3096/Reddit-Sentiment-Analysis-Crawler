CREATE TABLE `comment_sentiments` (
  `ticker` varchar(10) NOT NULL,
  `source` varchar(45) NOT NULL,
  `sentiment` decimal(10,5) DEFAULT NULL,
  `received` datetime NOT NULL,
  PRIMARY KEY (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stocks_list` (
  `ticker` varchar(10) NOT NULL,
  `fullname` varchar(45) NOT NULL,
  PRIMARY KEY (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `word_sentiments` (
  `word` varchar(50) NOT NULL,
  `sentiment` decimal(10,5) NOT NULL,
  PRIMARY KEY (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER 
VIEW `view_sentiments` AS 
	select `a`.`ticker` AS `Ticker`
    ,`b`.`fullname` AS `Company_Name`
    ,count(distinct `a`.`source`) AS `Number_Sources`
    ,count(0) AS `Number_Comments`
    ,avg(`a`.`sentiment`) AS `Sentiment`
    ,min(`a`.`received`) AS `Period_Beginning` 
    
    from (`comment_sentiments` `a` 
		join `stocks_list` `b` on((`a`.`ticker` = `b`.`ticker`))
	) 
    
    group by `a`.`ticker`,`b`.`fullname` 
    
    order by `Number_Comments` desc;
