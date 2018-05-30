args <- commandArgs(trailingOnly = TRUE)

newdata = data.frame(UserReputation=args[1],
					CodeSnippet=sapply(as.character(args[2]),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					Weekday=args[3], GMTHour=args[4], BodyLength =args[5],
					TitleLength=args[6], 
					URL=sapply(as.character(args[7]),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					AvgUpperCharsPPost=as.numeric(args[8]), 
					SentimentPositiveScore=sapply(as.character(args[9]),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					SentimentNegativeScore =sapply(as.character(args[10]),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					NTag=sapply(as.character(args[11]),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE))
					)

#print(args[1])
modello <- readRDS(file="modelloR.RDS")
prediction <- predict(modello, newdata, type="response")

print(prediction)


