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
## if you see the version is out of date, run: update.packages()

# install.packages("readxl")
# install.packages("ggplot2")
# install.packages("cowplot")

### LOADING PACKAGES ###
library("readxl")
library("ggplot2")
library("cowplot")


### CHECK CURRENT DIRECTORY LOCATION
getwd() 

# Load in Data for State 0/1/2, Jackal/Spot, Pre/Post Learning (All data combined)
regression_data <- read_excel("data/part2_classification/final_results/final_text.xlsx", sheet="ACCURACY_LOGIREG", range = "A1:J901", col_names = TRUE, col_types = NULL, na = "", skip = 0)

# Look at the data
head(regression_data)

# Remove the first and third column (Value and User ID)
regression_data_trim <- subset(regression_data, select = -c(1, 2, 6, 7, 8, 9))

# Look at the data structure (see what type of data is in each column)
str(regression_data_trim)

# DATA CLEANING
# Facotrs = catagorical data.
# In general, we want to convert ordinal data (which may appear as 'num') to catagorical ('factors')
# In this case, we dont have any ordinal data, so we dont need to convert anything
# We do however have 'chr' which needs to be changed to 'factors' (catagorical)

# Replace the binary 0/1 output for 'Correct' with "Correct" and "Incorrect" and change to factor
regression_data_trim$Correct <- ifelse(test=regression_data_trim$Correct == 1, yes="=Correct", no="=Incorrect")
regression_data_trim$Correct <- factor(regression_data_trim$Correct) # Now convert to a factor


# Change Part_One Y / N to factors (catagorical)
regression_data_trim[regression_data_trim$Part_One == "Y",]$Part_One <- "=Yes"
regression_data_trim[regression_data_trim$Part_One == "N",]$Part_One <- "=No"
regression_data_trim$Part_One <- factor(regression_data_trim$Part_One, levels=c("=No", "=Yes"))
# previously as.factor


# Change Condition GPT4 / Human / Random to factors (catagorical)
# Here we specify the levels to be in a specific order (Random Human GPT4) therefor random is the reference level
regression_data_trim[regression_data_trim$Condition == "Random",]$Condition <- "=Random"
regression_data_trim[regression_data_trim$Condition == "Human",]$Condition <- "=Human"
regression_data_trim[regression_data_trim$Condition == "GPT4",]$Condition <- "=GPT4"
regression_data_trim$Condition <- factor(regression_data_trim$Condition, levels=c("=Random", "=Human", "=GPT4"))

# Change Real_State names to be shorted and change to factors (catagorical)
# Here we dont specify the levels, so the levels will be in alphabetical order
regression_data_trim[regression_data_trim$Real_State == "Waiting for Input",]$Real_State <- "=Waitin."
regression_data_trim[regression_data_trim$Real_State == "Analyzing Object",]$Real_State <- "=AnaObj."
regression_data_trim[regression_data_trim$Real_State == "Found Object",]$Real_State <- "=FouObj."
regression_data_trim[regression_data_trim$Real_State == "Needs Help",]$Real_State <- "=NeedHel."
regression_data_trim[regression_data_trim$Real_State == "Confused",]$Real_State <- "=Confus."
regression_data_trim$Real_State <- factor(regression_data_trim$Real_State, levels=c("=Waitin.", "=AnaObj.", "=FouObj.", "=NeedHel.", "=Confus."))

# Look at the data structure again (see what type of data is in each column)
str(regression_data_trim)

# Good practice: check that there is a good amount of samples for correct and incorrect responses
table(regression_data_trim$Correct)

# Good practice: exclude variables that only have 1 or 2 samples in a category
# since +/- one or two samples can have a large effect on the odds/log(odds)
# We only need to do this for our data that is catagorical (not continuous)
xtabs(~ Correct + Part_One, data=regression_data_trim)
xtabs(~ Correct + Condition, data=regression_data_trim)
xtabs(~ Correct + Real_State, data=regression_data_trim)


# First let check if there are any interactions between our variables (A, B, C, AB, AC, BC, ABC)
interactions_logit <- glm(Correct ~ Part_One + Condition + Real_State + (Part_One*Condition) + (Part_One*Real_State) + 
                    (Condition*Real_State) + (Part_One*Condition*Real_State), data=regression_data_trim, family='binomial')
summary(interactions_logit)


# Now lets check for interactrion between the variables that are significant... 
# significant_interactions_logit <- glm(Correct ~ Condition + Real_State, data=regression_data_trim, family='binomial')
# summary(significant_interactions_logit)


# Now lets run a logistic regression using the glm function
# Lets look at the model with all variables
regression_logit <- glm(Correct ~ Part_One + Condition + Real_State + (Condition*Real_State),  data=regression_data_trim, family='binomial')
summary(regression_logit)

