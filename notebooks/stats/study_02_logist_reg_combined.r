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

# Load in Data for State 0/1/2, Section 2U/2I (All datasets combined -> 27 cubes x 24 users = 648 samples ... 648 x 6 = 3888 samples)
regression_data <- read_excel("notebooks/user_data/response_book.xlsx", sheet="regression_combined", range = "A1:I3889", col_names = TRUE, col_types = NULL, na = "", skip = 0)

# Look at the data
head(regression_data)

# Remove the 1st, 3rd and 7th column (Value, User ID, Confidence)
regression_data_trim <- subset(regression_data, select = -c(1, 3))

# Look at the data structure (see what type of data is in each column)
str(regression_data_trim)

# Currently our acoustic parameters are type 'num', we need to modify this
# Note: The next lines convert ordinal data to factors (catagorical)

# Replace the binary output for 'Positive_Val' with "=Positive Value" and "=Non-positive Value"
regression_data_trim$Positive_Val <- ifelse(test=regression_data_trim$Positive_Val == 1, yes="=Positive Value", no="=Non-positive Value")
regression_data_trim$Positive_Val <- as.factor(regression_data_trim$Positive_Val) # Now convert to a factor


# Note, we don't convert the confidence to a factor, since it is a continuous variable (0.0-10.0)
regression_data_trim$P1_BPM <- as.character(regression_data_trim$P1_BPM)
regression_data_trim[regression_data_trim$P1_BPM == '0',]$P1_BPM <- "=0"
regression_data_trim[regression_data_trim$P1_BPM == '1',]$P1_BPM <- "=1"
regression_data_trim[regression_data_trim$P1_BPM == '2',]$P1_BPM <- "=2"
regression_data_trim$P1_BPM <- as.factor(regression_data_trim$P1_BPM)


regression_data_trim$P2_BPL <- as.character(regression_data_trim$P2_BPL)
regression_data_trim[regression_data_trim$P2_BPL == '0',]$P2_BPL <- "=0"
regression_data_trim[regression_data_trim$P2_BPL == '1',]$P2_BPL <- "=1"
regression_data_trim[regression_data_trim$P2_BPL == '2',]$P2_BPL <- "=2"
regression_data_trim$P2_BPL <- as.factor(regression_data_trim$P2_BPL)

regression_data_trim$P3_Pitch <- as.character(regression_data_trim$P3_Pitch)
regression_data_trim[regression_data_trim$P3_Pitch == '0',]$P3_Pitch <- "=0"
regression_data_trim[regression_data_trim$P3_Pitch == '1',]$P3_Pitch <- "=1"
regression_data_trim[regression_data_trim$P3_Pitch == '2',]$P3_Pitch <- "=2"
regression_data_trim$P3_Pitch <- as.factor(regression_data_trim$P3_Pitch)

# Change States 0 / 1 / 2 to factors (catagorical)
regression_data_trim$State <- as.character(regression_data_trim$State)
regression_data_trim[regression_data_trim$State == '0',]$State <- "=Stuck"
regression_data_trim[regression_data_trim$State == '1',]$State <- "=Accom."
regression_data_trim[regression_data_trim$State == '2',]$State <- "=Progr."
regression_data_trim$State <- as.factor(regression_data_trim$State)

# Change Init U / I to factors (catagorical)
regression_data_trim[regression_data_trim$Init == "U",]$Init <- "=Uninformed"
regression_data_trim[regression_data_trim$Init == "I",]$Init <- "=Informed"
regression_data_trim$Init <- as.factor(regression_data_trim$Init)


# Look at the data structure again (see what type of data is in each column)
str(regression_data_trim)

# Good practice: check that there is a good amount of samples for Positive_Val and Non-positive_Val responses
table(regression_data_trim$Positive_Val)

# Good practice: exclude variables that only have 1 or 2 samples in a category
# since +/- one or two samples can have a large effect on the odds/log(odds)
# We only need to do this for our data that is catagorical (not continuous)
xtabs(~ Positive_Val + P1_BPM, data=regression_data_trim)
xtabs(~ Positive_Val + P2_BPL, data=regression_data_trim)
xtabs(~ Positive_Val + P3_Pitch, data=regression_data_trim)
xtabs(~ Positive_Val + State, data=regression_data_trim)
xtabs(~ Positive_Val + Init, data=regression_data_trim)


# Now lets run a logistic regression using the glm function
# Lets look at the model with all variables
regression_logit <- glm(Positive_Val ~ P1_BPM + P2_BPL + P3_Pitch + State + Init, data=regression_data_trim, family='binomial')
summary(regression_logit)


## QUICK DIVE INTO RESULTS
# BPM and BPL do not show a significant effect (p > 0.05)
# Pitch shows a significant effect (p < 0.05) 
# Confidence shows a significant effect (p < 0.05)
#
# Pitch and Confidence are both significant, so we shouldn't remove either of them from the model
# BPM and BPL are not significant, so we should remove them from the model
#
# Note that coefficients for Pitch are substantially larger than the coefficients for Confidence
## 



# Now calculate the overall "Pseudo R-squared" and its p-value
# Note: Since we are doing logistic regression...
#
#     Null devaince = 2*(0 - LogLikelihood(null model))
#                   = -2*LogLikihood(null model)
#
# Residual deviacne = 2*(0 - LogLikelihood(proposed model))
#                   = -2*LogLikelihood(proposed model)
#
# The null model is a model with only an intercept (no predictors)
 
ll.null <- regression_logit$null.deviance/-2  # Null model
ll.proposed <- regression_logit$deviance/-2   # Model w/ all parameters
 

# McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
# Note: This is a measure of model improvement (not model fit)
#       We can interpret Pseudo R^2 as the % improvement in model fit
(ll.null - ll.proposed) / ll.null


# Chi-square value = 2*(LL(Proposed) - LL(Null))
# p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq(2*(ll.proposed - ll.null), df=(length(regression_logit$coefficients)-1))

# Note that the resulting p-value is so tiny it is essentially zero (p < 0.0001)


# Now plot the data:
# Create a new dataframe that contains the predicted probabilities for each sample
predicted.regression_logit <- data.frame(
  probability.of.Positive_Val=regression_logit$fitted.values,
  Positive_Val=regression_data_trim$Positive_Val)

# Sort the data by the predicted probability
predicted.regression_logit <- predicted.regression_logit[
  order(predicted.regression_logit$probability.of.Positive_Val, decreasing=FALSE),]

# Add a column that contains the index of each sample
predicted.regression_logit$rank <- 1:nrow(predicted.regression_logit)

# Lastly, plot the predicted probabilities for each sample and colour each sample based on
# whether that sample is actually labeled as 'Positive_Val' or 'Non-positive_Val' 
ggplot(data=predicted.regression_logit, aes(x=rank, y=probability.of.Positive_Val)) +
  geom_point(aes(color=Positive_Val), alpha=1, shape=4, stroke=2) +
  xlab("Data Point Index") +
  ylab("Predicted Probability of Parameter Combinations \nhaving Positive Value at Convergence\n") +
    ggtitle("Logistic Regression for Parameter Combinations \nhaving Positive Value at Convergence\n") +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_color_manual(values=c("#40a100", "#ff6600")) +
    theme(legend.title=element_blank()) +
    theme(legend.position="bottom") +
    theme(legend.text=element_text(size=12)) +
    theme(axis.text.x=element_text(size=12)) +
    theme(axis.text.y=element_text(size=12)) +
    theme(axis.title.x=element_text(size=16)) +
    theme(axis.title.y=element_text(size=16)) +
    theme(plot.title=element_text(size=20))






















