import React, {Component} from 'react';
import {Grid, Button, ButtonGroup, Typography} from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from "react-router-dom";
import Quiz from "./Quiz";
import Recommendations from "./Recommendations";
import { Navigate } from 'react-router-dom';

export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            quizCode: null,
            spotifyAuthenticated: false,
        };
        this.clearQuizCode = this.clearQuizCode.bind(this);
    }

    async componentDidMount() {
        fetch('/api/user-in-quiz').then((response) => response.json()).then((data) => {
            this.setState({
                quizCode: data.code
            });
        });
    }

    renderHomePage() {
        if(this.state.quizCode) {
            return(
              <Navigate to={`/recc/${this.state.quizCode}`} replace={true} />
            )
        }
        else {
            return (
                <Grid container spacing={3}>
                    <Grid item xs={12} align="center">
                        <Typography variant="h3" component="h3">
                            Spotify Recommender
                        </Typography>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <ButtonGroup disableElevation variant="contained" color="primary">
                            <Button color="primary" to="/quiz" component={Link}>
                                Take the quiz
                            </Button>
                        </ButtonGroup>
                    </Grid>
                </Grid>
            );
        }
    }

    clearQuizCode() {
        this.setState({
            quizCode: null,    
        });
    }

    render() {
        return (
            <Router>
                <Routes>
                    <Route exact path="/" element={this.renderHomePage()} />
                    <Route path="/quiz" element={<Quiz />} />
                    <Route exact path="/recc/:quizCode/" element={<Recommendations />} render={({ match }) => <Quiz id={match.params.quizCode} />} />
                    <Route path="/room/:roomCode" element={<Quiz leaveQuiz={this.clearQuizCode} />}/>
                </Routes>
            </Router>
        );
    }

    /*
    <Route path="/room/:roomCode" render={(props) => <RoomWrapper {...props} clearQuizCode={clearQuizCode} />} />
    render() {
        return (
            <Router>
                <Routes>
                    <Route exact path="/" render={() => {
                        return this.state.quizCode ? (<Redirect to={`/room/${this.state.Code}`}></Redirect>) : this.renderHomePage()
                    }}></Route>
                    <Route path="/quiz" element={<Quiz />} />
                    <Route path="/recc/:quizCode" element={<Recommendations/>}/>
                </Routes>
            </Router>
        );
    }*/
}