library(plumber)
#api <- plumb("/var/www/qavmentor/R_service/api.R")
api <- plumb("./api.R")
api$run(port=1111)
