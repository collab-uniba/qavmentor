library(plumber)
#api <- plumb("/var/www/qavmentor/R_service/api.R")
list.files(path=paste(getwd(),"R_service",sep="/"))
api <- plumb(paste(getwd(),"R_service/api.R",sep="/")) #for testing on local host
api$run(port=1111)
