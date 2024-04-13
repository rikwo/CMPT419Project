import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {Grid, Button, Typography} from "@mui/material";
import {Link} from "react-router-dom"

export default function Recommendations() {
    const { quizCode } = useParams(); // Accessing the room code from the URL
    const [items, setItems] = useState({});
    const [state, setState] = useState({
            popularity: 1,
            danceability: 1,
            energy: 1,
            valence: 1,
            tempo: 100,
            spotifyAuthenticated: false,
        });

    const [quizPlaylist, setQuizPlaylist] = useState(null);
    const [recommendedPlaylist, setRecommendedPlaylist] = useState(null);

    const navigate = useNavigate()

    const leaveButtonPressed = () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        };
        fetch("/api/leave-quiz", requestOptions)
            .then((_response) => {
                // Perform any callback or state updates upon leaving the room
                //props.clearQuizCode();
                navigate("/"); // Navigate back to the home page
            })
            .catch((error) => {
                console.error("Error leaving room:", error);
            });
    };

    const recommendTopSongs = async () => {
        try {
            const response = await fetch(`/api/recommend-top-songs?quizCode=${quizCode}`);
            if (!response.ok) {
                console.error("Failed to fetch recommended songs.");
                return;
            }
            const data = await response.json();
            console.log("Recommended songs:", data);

            // After receiving recommended songs, redirect user to the home page or perform other actions
            navigate("/"); // Redirect to the home page
        } catch (error) {
            console.error("Error recommending top songs:", error);
        }
    };

    const authenticateSpotify = () => {
        fetch("/spotify/is-authenticated")
            .then((response) => response.json())
            .then((data) => {
                setState((prevState) => ({
                    ...prevState,
                    spotifyAuthenticated: data.status,
                }));
                console.log(data.status);
                if (!data.status) {
                    fetch("/spotify/get-auth-url")
                        .then((response) => response.json())
                        .then((data) => {
                            window.location.replace(data.url);
                        })
                        .catch((error) => {
                            console.error("Error fetching authentication URL:", error);
                        });
                }
            })
            .catch((error) => {
                console.error("Error checking authentication status:", error);
            });
    };

    const getSongs = () => {
        fetch("/spotify/tracks").then((response) => 
            {if (!response.ok) {
              return [];
            } else {
              return response.json();
            }
          })
          .then((data) => {
            setState((setItems) => ({
              items: data,
            }));
            console.log(data);
          });
      };


    useEffect(() => {
        async function getQuizDetails() {
          try {
            const response = await fetch(`/api/get-quiz?code=${quizCode}`);
            if (!response.ok) {
              // If response is not ok, leave the room and navigate to the home page
              leaveButtonPressed(); // Assume this function is defined correctly
              return;
            }
            const data = await response.json();
            setState((prevState) => ({
              ...prevState,
              popularity: data.popularity,
              danceability: data.danceability,
              energy: data.energy,
              valence: data.valence,
              tempo: data.tempo,
              spotifyAuthenticated: data.spotifyAuthenticated
            }));
            authenticateSpotify();
          } catch (error) {
            console.error("Error fetching room details:", error);
          }
        }
        getSongs();
        getQuizDetails(); // Call the async function immediately
      }, [quizCode]); // Trigger effect when quizCode changes

    

    useEffect(() => {
        // Call recommendTopSongs when Spotify authentication is successful
        if (state.spotifyAuthenticated) {
            recommendTopSongs();
        }
    }, [state.spotifyAuthenticated]);

    return (<Grid container spacing={1}>
        {state.items && state.items.length > 0 ? (
        state.items.map((item) => (
          <Grid item xs={3} key={item.track_id} align="center">
            <Typography variant="h6" component="h6">
              {item.name} by {item.artist}
            </Typography>
            <img src={item.album_cover} alt="Album Cover" />
            {/* Display other track information */}
          </Grid>
        ))
      ) : (
        <Grid item xs={12} align="center">
          <Typography variant="body1" component="p">
            No current song found.
          </Typography>
        </Grid>
      )}
        <Grid item xs={12} align="center">
            <Button variant="contained" color="secondary" onClick={leaveButtonPressed}>
                Restart
            </Button>
        </Grid>
    </Grid>);
    
}