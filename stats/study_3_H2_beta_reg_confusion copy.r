# Before starting, make sure you have opened a new terminal and typed: radian
# To run the entire script, type: Ctrl+Shift+S, for one line simply Ctrl+Enter
# To modify linter try this page: https://lintr.r-lib.org/articles/lintr.html#configuring-linters

# This script performs a logistic regression on the data from Study 2

# Reference Video (StatQuest)
# https://www.youtube.com/watch?v=C4N3_XJJ-jU&list=PLblh5JKOoLUKxzEP5HA2d-Li7IJkHfXSe&index=7&ab_channel=StatQuestwithJoshStarmer

# Reference Code (StatQuest)
# https://github.com/StatQuest/logistic_regression_demo/blob/master/logistic_regression_demo.R

# References for Explaining Output
# https://quantifyinghealth.com/logistic-regression-in-r-with-categorical-variables/
# https://towardsdatascience.com/simply-explained-logistic-regression-with-example-in-r-b919acb1d6b3
# https://stats.idre.ucla.edu/r/dae/logit-regression/


### INSTALLING PACKAGES ###
# Remove packages if they are misbehaving
# remove.packages("readxl")
# remove.packages("betareg")


### INSTALLING PACKAGES ###
## if you see the version is out of date, run: update.packages(ask = FALSE, checkBuilt = TRUE)
# install.packages("readxl")
# install.packages("ggplot2")
# install.packages("cowplot")
# install.packages("betareg")
# install.packages("coda")
# install.packages("rjags")
# install.packages("zoib")


### LOADING PACKAGES ###
library("readxl")
# library("ggplot2")
# library("cowplot")
library("betareg")
# library('rjags')
# library('zoib')



### CHECK CURRENT DIRECTORY LOCATION
getwd() 

# Load in Data for State 0/1/2, Jackal/Spot, Pre/Post Learning (All data combined)
regression_data <- read_excel("data/part1_collection/llm_generated_data.xlsx", sheet="distance_regr", range = "A1:I51", col_names = TRUE, col_types = NULL, na = "", skip = 0)

# Look at the data
head(regression_data)

# Remove the first and third column (Value and User ID) ~ omit swap 9/10 for adjusted/unadjusted
regression_data_trim <- subset(regression_data, select = -c(1, 4, 5, 7, 8)) 

# Look at the data structure (see what type of data is in each column)
str(regression_data_trim)

# DATA CLEANING
# Facotrs = catagorical data.
# In general, we want to convert ordinal data (which may appear as 'num') to catagorical ('factors')
# In this case, we dont have any ordinal data, so we dont need to convert anything
# We do however have 'chr' which needs to be changed to 'factors' (catagorical)


# Change condition LLM / Human to factors (catagorical)
regression_data_trim[regression_data_trim$condition == "LLM",]$condition <- "=LLM"
regression_data_trim[regression_data_trim$condition == "Human",]$condition <- "=Human"
regression_data_trim$condition <- factor(regression_data_trim$condition, levels=c("=Human", "=LLM"))

# Change real_state to factors (catagorical)
regression_data_trim[regression_data_trim$real_state == "Waiting for Input",]$real_state <- "=Waiting for Input"
regression_data_trim[regression_data_trim$real_state == "Analyzing Object",]$real_state <- "=Analyzing Object"
regression_data_trim[regression_data_trim$real_state == "Found Object",]$real_state <- "=Found Object"
regression_data_trim[regression_data_trim$real_state == "Needs Help",]$real_state <- "=Needs Help"
regression_data_trim[regression_data_trim$real_state == "Confused",]$real_state <- "=Confused"
regression_data_trim$real_state <- factor(regression_data_trim$real_state, levels=c("=Waiting for Input", "=Analyzing Object", "=Found Object", "=Needs Help", "=Confused"))


# Change selected_state to factors (catagorical)
# regression_data_trim[regression_data_trim$selected_state == "Waiting for Input",]$selected_state <- "=Waiting for Input"
# regression_data_trim[regression_data_trim$selected_state == "Analyzing Object",]$selected_state <- "=Analyzing Object"
# regression_data_trim[regression_data_trim$selected_state == "Found Object",]$selected_state <- "=Found Object"
# regression_data_trim[regression_data_trim$selected_state == "Needs Help",]$selected_state <- "=Needs Help"
# regression_data_trim[regression_data_trim$selected_state == "Confused",]$selected_state <- "=Confused"
# regression_data_trim$selected_state <- factor(regression_data_trim$selected_state, levels=c("=Waiting for Input", "=Analyzing Object", "=Found Object", "=Needs Help", "=Confused"))



# Look at the data structure again (see what type of data is in each column)
str(regression_data_trim)

# show all the values for confusion_transformed to ensure they all fall between 0 and 1 
unique(regression_data_trim$confusion_transformed)

# Apply is.na to each column and sum the results to check for any NA values (should return zero)
sum_na <- sapply(regression_data_trim, function(x) sum(is.na(x)))
sum_na

# Apply is.infinite to each column and sum the results to check for any infinite values
sum_infinite <- sapply(regression_data_trim, function(x) sum(is.infinite(x)))
sum_infinite


summary(regression_data_trim)

# Run the beta regression with test for interaction
regression_betareg <- betareg(confusion_transformed ~ condition + dist_value + real_state + (condition * dist_value) + (condition * real_state) + (dist_value * real_state) + (condition * dist_value * real_state), 
                            data=regression_data_trim)

summary(regression_betareg)


# Run the beta regression
regression_betareg <- betareg(confusion_transformed ~ condition + real_state + dist_value, 
                            data=regression_data_trim)

summary(regression_betareg)




