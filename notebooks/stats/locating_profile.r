candidates <- c( Sys.getenv("R_PROFILE"),
             file.path(Sys.getenv("R_HOME"), "etc", "Rprofile.site"),
             Sys.getenv("R_PROFILE_USER"),
             file.path(getwd(), ".Rprofile"),
             file.path(Sys.getenv("HOME"), ".Rprofile"))

Filter(file.exists, candidates)

candidates
