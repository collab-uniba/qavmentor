library(plumber)
#api <- plumb("/var/www/qavmentor/R_service/api.R")
api <- plumb(paste(getwd(),"api.R",sep="/")) #for testing on local host
api$run(port=1111)
