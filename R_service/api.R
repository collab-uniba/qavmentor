library("rjson")

modello <<- readRDS(file="/var/www/qavmentor/R_service/modelloR.RDS")
#modello <<- readRDS(paste(normalizePath(dirname(".")),"modelloR.RDS",sep="/")) #for testing windows

#* @post /model_predict
model_predict <- function(req) {
  cat(as.character(Sys.time()), "-", 
    req$REQUEST_METHOD, req$PATH_INFO, "-", "\n")
	json_data <- fromJSON(req$postBody)

	#cat("\n",json_data$CodeSnippet
	#,"\n",json_data$Weekday
	#,"\n",json_data$GMTHour
	#,"\n",json_data$BodyLength
	#,"\n",json_data$TitleLength
	#,"\n",json_data$URL
	#,"\n",json_data$AvgUpperCharsPPost
	#,"\n",json_data$SentimentPositiveScore
	#,"\n",json_data$SentimentNegativeScore
	#,"\n",json_data$NTag)
  	newdata <- data.frame(UserReputation=json_data$UserReputation,
					CodeSnippet=sapply(as.character(json_data$CodeSnippet),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					Weekday=json_data$Weekday, GMTHour=json_data$GMTHour, BodyLength=json_data$BodyLength,
					TitleLength=json_data$TitleLength, 
					URL=sapply(as.character(json_data$URL),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					AvgUpperCharsPPost=as.numeric(json_data$AvgUpperCharsPPost), 
					SentimentPositiveScore=sapply(as.character(json_data$SentimentPositiveScore),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					SentimentNegativeScore =sapply(as.character(json_data$SentimentNegativeScore),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE)), 
					NTag=sapply(as.character(json_data$NTag),switch,'False'=as.logical(FALSE),'True'=as.logical(TRUE))
					)


	prediction <- predict(modello, newdata, type="response")
	return(prediction)

}

