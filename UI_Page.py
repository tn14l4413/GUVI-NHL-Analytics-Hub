import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse

# ==========================================
# 1. PAGE CONFIGURATION & DATABASE CONNECTION
# ==========================================
st.set_page_config(
    page_title="NHL Analytics Hub",
    page_icon="🏒",
    layout="wide"
)

# URL encode the password safely
password = urllib.parse.quote_plus("Manoj1297@")

# Try with localhost
DB_URL = f"mysql+pymysql://root:{password}@127.0.0.1:3306/hockeyteam"
engine = create_engine(DB_URL)



@st.cache_resource
def get_db_engine():
    return create_engine(DB_URL)

engine = get_db_engine()

def run_query(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

# ==========================================
# 2. NAVIGATION SIDEBAR
# ==========================================
with st.sidebar:
    st.title("🏒 NHL Analytics Hub")
    selected_page = option_menu(
        menu_title="Main Menu",
        options=[
            "Home", 
            "Standings", 
            "Team Info", 
            "Player Search", 
            "Game Results", 
            "Leaderboards", 
            "SQL Query"
        ],
        icons=[
            "house-door", 
            "trophy", 
            "people-fill", 
            "search", 
            "calendar-event", 
            "award", 
            "database-gear"
        ],
        menu_icon="cast",
        default_index=0,
    )

# ==========================================
# 3. PAGE LOGIC
# ==========================================

# ------------------------------------------
# PAGE 1: HOME
# ------------------------------------------
if selected_page == "Home":
    st.title("🏒 Dashboard Overview")
    st.markdown("Real-time hockey analytics and statistical insights across teams, players, and games.")

    # High-level Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    teams_cnt = run_query("SELECT COUNT(*) AS total FROM nhl_teams")['total'][0]
    players_cnt = run_query("SELECT COUNT(*) AS total FROM nhl_players")['total'][0]
    games_cnt = run_query("SELECT COUNT(*) AS total FROM nhl_games")['total'][0]
    goals_cnt = run_query("SELECT SUM(goals) AS total FROM nhl_skater_season_stats")['total'][0] or 0

    with col1:
        st.metric("Total Teams", teams_cnt)
    with col2:
        st.metric("Active Players", players_cnt)
    with col3:
        st.metric("Games Tracked", games_cnt)
    with col4:
        st.metric("Total Goals Scored", int(goals_cnt))

    st.divider()

    # Highlight Stats
    st.subheader("🌟 Season Highlights")
    col_top1, col_top2 = st.columns(2)

    with col_top1:
        top_skater = run_query("""
            SELECT CONCAT(p.first_name, ' ', p.last_name) AS name, t.team_abbrev, s.points, s.goals, s.assists
            FROM nhl_skater_season_stats s
            JOIN nhl_players p ON s.player_id = p.player_id
            JOIN nhl_teams t ON s.team_id = t.team_id
            ORDER BY s.points DESC LIMIT 1
        """)
        if not top_skater.empty:
            st.info(f"**Top Point Scorer:** {top_skater['name'][0]} ({top_skater['team_abbrev'][0]})\n\n"
                    f"**{top_skater['points'][0]}** Points ({top_skater['goals'][0]} G, {top_skater['assists'][0]} A)")

    with col_top2:
        top_goalie = run_query("""
                    SELECT CONCAT(p.first_name, ' ', p.last_name) AS name, t.team_abbrev, g.save_pct, g.wins
                    FROM nhl_goalie_season_stats g
                    JOIN nhl_players p ON g.player_id = p.player_id
                    JOIN nhl_teams t ON g.team_id = t.team_id
                    WHERE g.games_played >= 10
                    ORDER BY g.save_pct DESC LIMIT 1
                """)
        if not top_goalie.empty:
            st.success(f"**Best Save Percentage:** {top_goalie['name'][0]} ({top_goalie['team_abbrev'][0]})\n\n"
                       f"**{top_goalie['save_pct'][0]:.3f}** SV% ({top_goalie['wins'][0]} Wins)")

# ------------------------------------------
# PAGE 2: STANDINGS
# ------------------------------------------
elif selected_page == "Standings":
    st.title("🏆 League Standings")
    
    # Conference & Division Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        conferences = ["All"] + list(run_query("SELECT DISTINCT conference_name FROM nhl_teams WHERE conference_name IS NOT NULL")['conference_name'])
        selected_conf = st.selectbox("Filter by Conference", conferences)
    
    with col_f2:
        divisions = ["All"] + list(run_query("SELECT DISTINCT division_name FROM nhl_teams WHERE division_name IS NOT NULL")['division_name'])
        selected_div = st.selectbox("Filter by Division", divisions)

    # Dynamic SQL query building
    query = """
        SELECT 
            t.logo_url,
            t.team_name AS Team,
            t.conference_name AS Conference,
            t.division_name AS Division,
            s.games_played AS GP,
            s.wins AS W,
            s.losses AS L,
            s.ot_losses AS OT,
            s.points AS PTS,
            s.goals_for AS GF,
            s.goals_against AS GA
        FROM nhl_standings s
        JOIN nhl_teams t ON s.team_id = t.team_id
        WHERE 1=1
    """
    params = {}
    if selected_conf != "All":
        query += " AND t.conference_name = :conf"
        params["conf"] = selected_conf
    if selected_div != "All":
        query += " AND t.division_name = :div"
        params["div"] = selected_div

    query += " ORDER BY s.points DESC, s.wins DESC"

    df_standings = run_query(query, params)
    
    # Render with images in dataframe if logos available
    st.dataframe(
        df_standings,
        column_config={
            "logo_url": st.column_config.ImageColumn("Logo", help="Team Logo")
        },
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------
# PAGE 3: TEAM INFO
# ------------------------------------------
elif selected_page == "Team Info":
    st.title("🛡️ Team Details & Roster")

    teams_df = run_query("SELECT team_id, team_name, team_abbrev, conference_name, division_name, logo_url FROM nhl_teams")
    team_selected_name = st.selectbox("Select Team", teams_df['team_name'])
    
    team_data = teams_df[teams_df['team_name'] == team_selected_name].iloc[0]

    # Team Overview Header
    header_col1, header_col2 = st.columns([1, 4])
    with header_col1:
        if pd.notna(team_data['logo_url']):
            st.image(team_data['logo_url'], width=120)
    with header_col2:
        st.subheader(f"{team_data['team_name']} ({team_data['team_abbrev']})")
        st.write(f"**Conference:** {team_data['conference_name']} | **Division:** {team_data['division_name']}")

    st.divider()
    st.subheader("Team Roster")

    roster_df = run_query("""
        SELECT 
            headshot_url,
            CONCAT(first_name, ' ', last_name) AS player_name,
            position,
            jersey_number,
            shoots_catches,
            birth_country
        FROM nhl_players
        WHERE team_id = :team_id
        ORDER BY position, jersey_number
    """, {"team_id": int(team_data['team_id'])})

    st.dataframe(
        roster_df,
        column_config={
            "headshot_url": st.column_config.ImageColumn("Photo"),
            "player_name": "Player Name",
            "position": "Pos",
            "jersey_number": "#",
            "shoots_catches": "Shoots/Catches",
            "birth_country": "Country"
        },
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------
# PAGE 4: PLAYER SEARCH
# ------------------------------------------
elif selected_page == "Player Search":
    st.title("🔍 Player Search & Profile")

    search_term = st.text_input("Enter Player Name", placeholder="e.g., Connor McDavid")

    if search_term:
        players = run_query("""
            SELECT p.player_id, CONCAT(p.first_name, ' ', p.last_name) AS name, p.position, t.team_name
            FROM nhl_players p
            JOIN nhl_teams t ON p.team_id = t.team_id
            WHERE CONCAT(p.first_name, ' ', p.last_name) LIKE :search
        """, {"search": f"%{search_term}%"})

        if not players.empty:
            selected_player_id = st.selectbox(
                "Select Matching Player", 
                options=players['player_id'],
                format_func=lambda x: players[players['player_id'] == x]['name'].values[0] + " (" + players[players['player_id'] == x]['team_name'].values[0] + ")"
            )

            # Player Profile Details
            profile = run_query("""
                SELECT p.*, t.team_name 
                FROM nhl_players p 
                JOIN nhl_teams t ON p.team_id = t.team_id 
                WHERE p.player_id = :pid
            """, {"pid": int(selected_player_id)}).iloc[0]

            col_img, col_info = st.columns([1, 3])
            with col_img:
                if pd.notna(profile['headshot_url']):
                    st.image(profile['headshot_url'], width=150)
            with col_info:
                st.subheader(f"{profile['first_name']} {profile['last_name']} #{profile['jersey_number']}")
                st.write(f"**Team:** {profile['team_name']} | **Position:** {profile['position']}")
                st.write(f"**Height:** {profile['height_cm']} cm | **Weight:** {profile['weight_kg']} kg | **Shoots:** {profile['shoots_catches']}")

            # Load Player Stats depending on Position
            st.divider()
            if profile['position'] == 'G':
                g_stats = run_query("SELECT * FROM nhl_goalie_season_stats WHERE player_id = :pid", {"pid": int(selected_player_id)})
                st.dataframe(g_stats, use_container_width=True, hide_index=True)
            else:
                s_stats = run_query("SELECT * FROM nhl_skater_season_stats WHERE player_id = :pid", {"pid": int(selected_player_id)})
                st.dataframe(s_stats, use_container_width=True, hide_index=True)
        else:
            st.warning("No players found matching your search term.")

# ------------------------------------------
# PAGE 5: GAME RESULTS
# ------------------------------------------
elif selected_page == "Game Results":
    st.title("📅 Game Results & Schedule")

    col1, col2 = st.columns(2)
    with col1:
        game_state = st.selectbox("Game State", ["All", "OFF", "FUT", "LIVE"])
    with col2:
        team_filter = st.selectbox("Team Filter", ["All"] + list(run_query("SELECT team_name FROM nhl_teams")['team_name']))

    query = """
        SELECT 
            g.game_date AS Date,
            ht.team_name AS Home_Team,
            g.home_score AS Home_Score,
            g.away_score AS Away_Score,
            at.team_name AS Away_Team,
            g.game_state AS State,
            g.venue_name AS Venue
        FROM nhl_games g
        JOIN nhl_teams ht ON g.home_team_id = ht.team_id
        JOIN nhl_teams at ON g.away_team_id = at.team_id
        WHERE 1=1
    """
    params = {}
    if game_state != "All":
        query += " AND g.game_state = :state"
        params["state"] = game_state
    if team_filter != "All":
        query += " AND (ht.team_name = :team OR at.team_name = :team)"
        params["team"] = team_filter

    query += " ORDER BY g.game_date DESC LIMIT 100"

    games_df = run_query(query, params)
    st.dataframe(games_df, use_container_width=True, hide_index=True)

# ------------------------------------------
# PAGE 6: LEADERBOARDS
# ------------------------------------------
elif selected_page == "Leaderboards":
    st.title("🏅 Season Leaderboards")

    tab1, tab2, tab3 = st.tabs(["Top Point Scorers", "Most Goals", "Goalie Leaders"])

    with tab1:
        df_pts = run_query("""
            SELECT CONCAT(p.first_name, ' ', p.last_name) AS Player, t.team_abbrev AS Team, s.points AS Points, s.goals AS Goals, s.assists AS Assists
            FROM nhl_skater_season_stats s
            JOIN nhl_players p ON s.player_id = p.player_id
            JOIN nhl_teams t ON s.team_id = t.team_id
            ORDER BY s.points DESC LIMIT 10
        """)
        st.dataframe(df_pts, use_container_width=True, hide_index=True)

    with tab2:
        df_goals = run_query("""
            SELECT CONCAT(p.first_name, ' ', p.last_name) AS Player, t.team_abbrev AS Team, s.goals AS Goals, s.shots AS Shots
            FROM nhl_skater_season_stats s
            JOIN nhl_players p ON s.player_id = p.player_id
            JOIN nhl_teams t ON s.team_id = t.team_id
            ORDER BY s.goals DESC LIMIT 10
        """)
        st.dataframe(df_goals, use_container_width=True, hide_index=True)

    with tab3:
        df_goalies = run_query("""
            SELECT CONCAT(p.first_name, ' ', p.last_name) AS Player, t.team_abbrev AS Team, g.wins AS Wins, g.save_pct AS Save_Pct, g.shutouts AS Shutouts
            FROM nhl_goalie_season_stats g
            JOIN nhl_players p ON g.player_id = p.player_id
            JOIN nhl_teams t ON g.team_id = t.team_id
            ORDER BY g.wins DESC LIMIT 10
        """)
        st.dataframe(df_goalies, use_container_width=True, hide_index=True)

# ------------------------------------------
# PAGE 7: SQL QUERY EXECUTOR
# ------------------------------------------
elif selected_page == "SQL Query":
    st.title("💻 Custom SQL Query Console")

    preset_queries = {
        "Top 5 Point Scorers": "SELECT CONCAT(p.first_name, ' ', p.last_name) AS Name, s.points FROM nhl_skater_season_stats s JOIN nhl_players p ON s.player_id = p.player_id ORDER BY s.points DESC LIMIT 5",
        "Teams with Most Wins": "SELECT t.team_name, s.wins FROM nhl_standings s JOIN nhl_teams t ON s.team_id = t.team_id ORDER BY s.wins DESC",
        "Goalies with > 90% Save Pct": "SELECT CONCAT(p.first_name, ' ', p.last_name) AS Name, g.save_pct FROM nhl_goalie_season_stats g JOIN nhl_players p ON g.player_id = p.player_id WHERE g.save_pct > 0.900 ORDER BY g.save_pct DESC"
    }

    selected_preset = st.selectbox("Select Preset Query", ["Custom..."] + list(preset_queries.keys()))

    if selected_preset != "Custom...":
        default_sql = preset_queries[selected_preset]
    else:
        default_sql = "SELECT * FROM nhl_teams LIMIT 10;"

    sql_input = st.text_area("SQL Query Input", value=default_sql, height=120)

    if st.button("Run Query"):
        try:
            results = run_query(sql_input)
            st.success(f"Query returned {len(results)} rows.")
            st.dataframe(results, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {e}")