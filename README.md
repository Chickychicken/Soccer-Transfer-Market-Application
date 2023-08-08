# Soccer Transfer Market Application

Project by Bofei He

# Table of Contents
- Introduction
- Obtaining Data & Cleaning
- Value Model Training and Testing
- Player Performance Projection
- Recommendation System
- Streamlit App
- Contributor

# Introduction
The football industry has experienced an unprecedented surge in revenue, driven by lucrative sponsorship deals, TV broadcasting contracts, and substantial investments from affluent team owners. Consequently, the soccer transfer market has witnessed an astronomical inflation of player valuations over the past decade. However, the year 2023 proved to be a defining moment when the Saudi Arabian League clubs made headlines by surpassing all prior records with astonishing offers. Among these was a groundbreaking proposal to Kylian Mbappe, a renowned football sensation, with an audacious reported annual salary of £700 million. This remarkable transfer not only set a new benchmark for player valuations but also triggered a paradigm shift, reshaping the dynamics of the entire market.

Amidst this backdrop of financial extravagance and soaring player prices, there arises an imperative for innovative solutions to navigate this ever-evolving soccer transfer landscape effectively. In response to these challenges and opportunities, we embarked on the development of a pioneering Soccer Transfer Market Application. This application aims to revolutionize how clubs, agents, and football enthusiasts interact with player data. Through this report, we delve into the design, development, and key functionalities of our Soccer Transfer Market Application, shedding light on the methodologies utilized in its creation. We aim to provide valuable insights into the transformative soccer transfer landscape, underscoring the significance of data-driven decision-making in this hypercompetitive domain, ultimately empowering stakeholders to make more informed and strategic player transfer decisions.

# Obtaining Data

In this project, two sources of data was scraped and used:
- FBREF - Detailed on-feild statistics of player performance
- Transfermarkt - Information regarding player transfer values

FBREF
FBREF is a widely popular website offering comprehensive statistical data for football matches, leagues, and players from various competitions worldwide. With an extensive database covering major domestic leagues, international tournaments, and continental games, FBREF provides in-depth player and team statistics, including goals, assists, shots, passes, tackles, interceptions, and advanced metrics like expected goals (xG) and expected assists (xA).

While the website does consist of data for player performances from many leagues across the globe, the leagues that had the most comprehensive data were the Premier League, La liga, Serie A, Bundesliga, Ligue 1, Liga Portugal, Eredivisie, Süper Lig, and Jupiler Pro League. Hence, I will be gathering data from each of the 9 leagues over the 2022-2023 season.

For each league, there are 10 different datasets measuring various facets of a player;s game. The datasets are named as follows:
- Standard Stats
- Goalkeeping
- Advanced Goalkeeping
- Shooting
- Passing
- Pass Types
- Goal and Shot Creation
- Defensive Actions
- Possession
- Miscellaneous Stats

Given that Goalkeepers are judged based on entirely different metrics when compared to outfield players, I decided to not include goalkeepers in this project. Therefore, the two datasets related to Goalkeeper performance will not be scraped.

Below is an overview of the remaining datasets:
- Standard Stats: As its name implies, this dataset consists of standard information about each player’s age, playing time and other basic information like goals scored and assisted, expected goals and assists, number of yellow/red cards etc.

- Shooting: Information regarding players’ shots from a quantitative as well as qualitative standpoint.

- Passing: Information regarding the quantity and quality of passes cumulatively as well as separated into sections based on pass distance (i.e. Short, Medium and Long distances)

- Pass Types: Information regarding the type of passes attempted and their respective outcomes (i.e. aerial/medium-level/ground level height and body part used to make the pass). In order to limit an already high number of features to use; this dataset was not utilized as it was decided based on domain knowledge that the body parts used by a player to make a pass or the height at which players make passes are unlikely to be a major determinant of a player’s price.

- Goal and Shot Creation: Information regarding players’ actions that have led to shot taking opportunities and goals.

- Defensive Actions: Information regarding the defensive aspects of a player’s game and also information about how their defensive efforts contributed to the team winning the ball back and creating a goal-scoring opportunity for the team as a result.

- Possession: Information regarding the player’s ability to progress the ball and impact the proceedings of the game.

- Miscellaneous Stats: Miscellaneous on-field performance information such as number of direct red cards, second yellow cards, fouls committed/drawn, offsides etc.

# Scraping FBREF
Since the website no longer supports an easy option to download the data, I implemented two functions with the Beautiful Soup library that allows me to scrape data automatically(See Notebook). The first function is called get_league_links(). When given the link of each league’s page, It locates and returns the link of each individual team in that league. Then, I implemented the scrape_players() function. This function iterates through each team’s link to locate and scrape out every player’s name and statistics from each of the tables highlighted above. After each league’s link was scraped, I combined and exported them into one csv file.

# Transfermarkt
Transfermarkt is a prominent online platform for football enthusiasts, offering a comprehensive database of transfer news, player valuations, statistics, and market trends. Founded in Germany in 2000, it has become one of the largest football databases globally, providing estimated market values for players, up-to-date transfer news and rumors, detailed player and club profiles, market value development tracking, transfer history, and national team statistics. Transfermarkt serves as an invaluable resource for football fans, clubs, agents, and journalists seeking insights into player values, transfer activities, and the latest happenings in the footballing world.

The information that I gathered from this website are:
Player Name
Current Team
Age
Position
Market Value 2023
Market Value 2022
I gathered two transfer values because the statistics of the 2022-2023 season can only determine how much that value has changed since 2022. The value in 2022 is determined from the player’s performance in previous years.

# Scraping Transfermarkt
Similar to FBREF, the website doesn’t support a download option. Therefore, I implemented some functions with the Beautiful Soup library that allows me to scrape data automatically(See Notebook). The first function is team_names(). This allows me to find the name of each team that’s in each league. Next, using the function team_links(). From the names of each team in a specific league, I was able to get a list of links for these teams. Finally, the function build_df. This function iterates through the links of each team to find and scrape every single player(on that team) and their desired statistics. This process was applied to each league as well as both 2023 and 2022. However in 2022, I only scraped the player names and market values. After scraping, I combined every league’s dataframe and changed the data type of player market values from object to integer. Then,  I subtracted each player’s 2022 market values from their 2023 dataset’s market values to create the final dataset for Transfermarkt.	

# Cleaning(Notebook)
Before combining the player statistics from FBREF and Transfermarkt, I had to fix some issues and formats. First, I used the unicode encoder to remove all special characters in players’ names. After that, I noticed that on FBREF, the player’s last name was listed first, and first name was listed second. I had to swap every single player’s first and last name. Then I checked for duplicated names and dropped every single duplicated player names. For the players that played on two different teams in one season. I kept the row that played the most games and dropped the other. Finally, I combined the two datasets and obtained my final dataset. Phew!

# Scraping and Cleaning Improvements
Some improve in scraping and cleaning include:
Many players were bought from smaller leagues during this period. In addition, many players left bigger leagues. So I lost some data points because of this. Next time, I think I should scrape every single player in 2023 and scrape each of those players’ market value by iterating through their names instead of scraping with team links.
Combining the stats and matches played for duplicated players. This is hard to do because some stats are per 90 minutes or percentages so I have to recompute these stats from other stats.

# Value Model Training and Testing
## Workflow
Given my assumption that player values are likely determined by different attributes based on their playing position, a model was built for each of the 3 positions: attackers, midfielder and defenders. In each notebook, it can be seen that a modeling workflow to predict transfer values was first created for the attacking players’ dataset. Once a workflow had been established, the same process of modeling steps and printing results was repeated for midfielders and defenders.

## Models
Five different models were used to help predict players’ change in transfer values. In each model, the models were first used with their default hyperparameters. The first modeling attempt in each workflow would use the features that are most related to the players’ positions. For example, attackers include goals, shots on target, goal creating actions, and etc. Midfielders include pass completion, assists, total passing distances, and etc. Defenders include interceptions, clearances, tackles, and etc. However, all of these player groups have some attributes in common. These are age and matches played. Once the initial model was run, a second model was run by transforming and removing some variables to avoid collinearity. For transformation, I used the power transformer. For removing variables, I checked the variance inflation factor(VIF) which is a statistical measure used in regression analysis to assess multicollinearity between predictor variables. After that, I conducted a grid search with some hyperparameter tuning to find the best parameters. Finally, the model was fitted with these hyperparameters. To evaluate my model’s performance, Root Mean Square Error(RMSE) was calculated. RMSE is a common metric used to evaluate the performance of a predictive model. It is a measure of the differences between predicted values and actual (observed) values in a dataset. It calculates the square root of the average of the squared differences between predicted and actual values. 

A lower RMSE indicates that the model's predictions are closer to the actual values, signifying better performance. Conversely, a higher RMSE suggests that the model's predictions deviate more from the actual values, indicating poorer performance.

Here is a list of the models that I used:
Decision Trees Regression
Easy to interpret and handle non-linearity well
Prone to overfitting
Random Forest Regression
Improved accuracy since it combines multiple decision trees
Understanding the exact reasoning behind each prediction is challenging
Gradient Boost
Combines predictions of weak learners that reduce bias and variance to improve model performance
Finding the right combination of hyperparameters can be challenging, and different sets of hyperparameters may result in significantly different model performances. 
ElasticNet Regression
Combines strengths of Lasso and Ridge regression to handle high-dimensional datasets
Lasso helps removes irrelevant features
Ridge helps reduce the impact of multicollinearity among features
Improper hyperparameter tuning may lead to suboptimal results, with the model not fully exploiting the benefits of both L1 and L2 regularization.
Support Vector Regression
Robust to outliers since it finds hyperplane that best first the majority of data
Model is very complex and it’s time consuming to find the optimal parameters

Below are the performance of each model for each positions:



Decision Tree Regression(Notebook)

Random Forest Regression(Notebook)

Gradient Boost Regression(Notebook)


Elastic Net Regression(Notebook)

Support Vector Regression(Notebook)


## Model Evaluation(Notebook)
Having concluded modeling for this part of the project, the results for each model were compared to identify which model worked best to predict players’ change in transfer values with the lowest RMSE for each position.


Random Forest produced the lowest RMSE for attackers

ElasticNet produced the lowest RMSE for midfielders

Random Forest produced the lowest RMSE for defenders

My models have an error of around 6 - 10 million euros. Although defenders’ RMSE is the lowest, defenders are cheaper compared to attackers and midfielders so therefore my models’ performances are around the same regardless of position.

As for the attributes that determines the players’ change in price the most, here are the top 3 for each position:
Attackers:
Age
Goal Creating Actions
Shots on Target %
Midfielders:
Age
Total Passing Distance
Goals
Defenders:
Age
Progressive Passing Distance
Successful Challenge %
For all 3 positions, age approximately doubles the second highest attribute. This means that age is the biggest factor when it comes to predicting how much a player’s market transfer value has changed.

## Model testing
I generated 10 random players from each of the 3 positions to see how their predicted values compare to their actual values. The results are solid.
Attackers

Midfielders

Defenders

The results are surprisingly good, especially for defenders! For the players that the predicted value deviates by more than 5 million, they are worth substantially more than the rest of the players to begin with. Since they have higher values to begin with, they have a higher bar on their performance. They are the best among the best so a bad season for them is still better than a good season for the average players. In addition, the model evaluates everyone’s performance the same. This explains why Mo Salah’s value is off by almost 25 million.

## Conclusion
Age stands out as the most crucial factor when predicting the change in transfer value across all positions. For attackers and defenders, the Random Forest regression model proves to be the most effective in accurately forecasting value fluctuations. On the other hand, when it comes to midfielders, the ElasticNet model outperforms others in predicting their value changes.
Overall, these models demonstrate decent accuracy in projecting value shifts for the majority of players. However, they may encounter challenges when dealing with star players or big names. This can be attributed to the high expectations people have for these players due to their stellar past performances. As a result, the models might not perform as well in capturing the nuances of value changes for these top-tier athletes.

## Model Improvements
Although the models did a decent job at predicting the awards, there are many drawbacks:
The assumption that all leagues in the competition are equally competitive is not true. This can be fixed by building a model for each league separated by positions. To gather enough data for thorough analysis to achieve this, it is essential to gather player data from multiple seasons, spanning at least five years, for each league. 
In the modern game, player positions are not divided into only 3 categories, there are a diverse set of player roles within each position, so data will need to be divided to factor this in. This also means a lot more data must be scraped.
Difference in performance standard for average and star players. This can be fixed by including the current transfer value of the players. A higher transfer value should mean higher performance standard while a lower transfer value should mean lower performance standard.
Variable selection in this analysis focuses solely on the statistics that are relevant to each player's specific position. When reducing collinearity, the attributes being removed are the ones that are highly correlated with each other. This can be optimized in a more rigorous way by applying principal component analysis.
Media Influence also plays a part. If a player is on a mainstream team or is hyped up to become the next GOAT, they are more likely to be over valued. This is hard to be factored in as the model only looks at the numbers. One potential way is to create a new column called popularity that uses sentiment analysis of top soccer news sites to evaluate a popularity score of each player.
What’s next?
Although the model performed well, it can definitely be improved to perform at a higher level. One major obstacle that I need to pass is data scraping. The more data that I have, the more accurate my models are and the more options I have in terms of grouping players. Therefore, the first step of improvement is to develop a more efficient way to scrape data from FBREF and Transfermarkt.

# Player Performance Projection


