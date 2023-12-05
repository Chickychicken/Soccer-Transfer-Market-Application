import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Load Model (replace this with your actual model loading code)
recommender_ed = joblib.load(open('./Similarity Model/recommender_ed_model.pkl', 'rb'))
recommender_cos = joblib.load(open('./Similarity Model/recommender_cos_model.pkl', 'rb'))

# Define model names
model_names = ['Replacement Model', 'Talent Model']

# Load dataset
data = pd.read_csv('./Similarity Model/Fifa_stats.csv')

# Extract a column containing player names
players = data['Player'].tolist()

# For output purposes
df_name = data['Player']
df_age = data['Age']
df_club = data['Club']
df_position = data['Position']
df_value = data['Value']

def recommend_player(selected_player, model):
    player = selected_player
    input_player_stats = data[data['Player'] == player][['Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']]

    if model == 'Replacement Model':
        model = recommender_ed
    else:
        model = recommender_cos
    
    distances, indices = model.kneighbors(input_player_stats)

    # Calculate similarity scores for each player
    similarity_scores = 1 / (1 + distances*0.01)

    # Create a DataFrame to display the results
    if model == recommender_ed:
        similar_players_df = pd.DataFrame({
            'Player': df_name[indices[0]],
            'Similarity Score%': (similarity_scores[0]*100).round(2),
            'Position': df_position[indices[0]],
            'Age': df_age[indices[0]],
            'Club': df_club[indices[0]],
            'Value': df_value[indices[0]]
        })
    else:
        similar_players_df = pd.DataFrame({
            'Player': df_name[indices[0]],
            'Similarity Score%': (similarity_scores[0]*1000000%100).round(2),
            'Position': df_position[indices[0]],
            'Age': df_age[indices[0]],
            'Club': df_club[indices[0]],
            'Value': df_value[indices[0]]
        })
    # Sort the DataFrame based on similarity scores in descending order
    if model == recommender_ed:
        similar_players_df = similar_players_df.sort_values(by='Similarity Score%', ascending=False)
    else:
        similar_players_df = similar_players_df.sort_values(by='Age', ascending=True)
        similar_players_df = similar_players_df.head(11)
    similar_players_df = similar_players_df.reset_index(drop=True)
    return similar_players_df

def radar_chart(selected_player, selected_player2):
    # Sample data
    variables = ['Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']
    values = data[data['Player'] == selected_player][['Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']]
    values = values.iloc[0].tolist()

    values2 = data[data['Player'] == selected_player2][['Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']]
    values2 = values2.iloc[0].tolist()

    # Number of variables
    num_vars = len(variables)

    # Calculate the angle at which each variable will be placed on the radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    # Close the radar chart by repeating the first data point
    values = np.concatenate((values, [values[0]]))
    values2 = np.concatenate((values2, [values2[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    # Set the figure size
    plt.figure(figsize=(8, 8))

    # Plot the radar chart
    plt.polar(angles, values, marker='o', label = selected_player)
    plt.fill(angles, values, alpha=0.25)
    plt.polar(angles, values2, marker='o', label = selected_player2)
    plt.fill(angles, values2, alpha=0.25)

    # Set the angle ticks and labels
    plt.xticks(angles[:-1], variables)

    # Set the plot title
    plt.title('Player Comparison')

    plt.ylim(0, 100)

    #for i in range(num_vars):
    #    plt.text(angles[i], values[i], str(values[i]), ha='right', va='top')

    for i in range(num_vars):
        plt.text(angles[i], values2[i], str(values2[i]), ha='left', va='bottom')

    plt.legend(loc='upper right')
    
    # Show the plot
    plt.show()

def main(title="Player Recommender".upper()):
    # Center-align the title
    st.markdown(
        "<h1 style='text-align: center; font-size: 65px; color: #4682B4;'>{}</h1>".format(
            title
        ),
        unsafe_allow_html=True,
    )

    # Center-align the image
    st.image("./screenshots/cover.jpeg", use_column_width=True)

    # Add content to the app
    st.write("Welcome to my Soccer Player Recommender App!")

    # Create the dropdown menu to select model
    selected_model = st.selectbox('Select a model', model_names)

    # Create the dropdown menu to select players
    selected_player = st.selectbox('Select a player', players)
    recommendations = recommend_player(selected_player, selected_model)
    st.write("Recommendations for", selected_player, ":", recommendations.iloc[1:])
        
    # Display the button to generate the radar chart
    selected_player2 = st.selectbox('Select a player', recommendations.iloc[1:])
    if st.button('Get Chart'):
        radar_chart(selected_player, selected_player2)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot() 
 

if __name__ == "__main__":
    main()
