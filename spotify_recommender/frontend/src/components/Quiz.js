import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Button from "@mui/material/Button";
import Slider from "@mui/material/Slider"
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import {Link} from "react-router-dom";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import { useNavigate } from "react-router-dom";

export default function Quiz(props) {


    const [popularity, setPopularity] = useState(1);
    const [danceability, setDanceability] = useState(1);
    const [energy, setEnergy] = useState(1);
    const [valence, setValence] = useState(1);
    const [tempo, setTempo] = useState(100);

    const navigate = useNavigate();


    const handlePopularity = event => {
        const newValue = parseInt(event.target.value, 10);
        setPopularity(newValue);
    }

    const handleDanceability = event => {
        const newValue = parseInt(event.target.value, 10);
        setDanceability(newValuee);
    }

    const handleEnergy = event => {
        const newValue = parseInt(event.target.value, 10);
        setEnergy(newValue);
    }

    const handleValence = event => {
        const newValue = parseInt(event.target.value, 10);
        setValence(newValue);
    }

    const handleTempo = event => {
        const newValue = parseInt(event.target.value, 10);
        setTempo(newValue);
    }

    const requestOptions = {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            popularity: popularity,
            danceability: danceability,
            energy: energy,
            valence: valence,
            tempo: tempo,
        }),
    };

    const handleSaveButtonPressed = () => {
        console.log(requestOptions)
        fetch('/api/create-quiz', requestOptions).then((response) => response.json()).then((data) => navigate('/recc/'+data.code))
    };

    return <Grid container spacing={1} sx={{p: 3}}>
        <Grid item xs={11} align="left">
            <Typography component='h3' variant='h3'>
                Preference Quiz
            </Typography>
        </Grid>
        <Grid item xs={12} align="left">
            <FormControl component="fieldset">
                <Typography component='h6' variant='h6'>
                    <div align='left'>
                        Do you prefer popular music? Give a rating from 0 to 10.
                    </div>
                </Typography>
                <TextField 
                    id="popularity"
                    type="number"
                    defaultValue={popularity}
                    inputProps={{min:0, max:10}}
                    onChange={handlePopularity}
                />
            </FormControl>
        </Grid>
        <Grid item xs={12} align="left">
            <FormControl component="fieldset">
                <Typography component='h6' variant='h6'>
                    <div align='left'>
                        Do you prefer music you can dance to? Give a rating from 0 to 10.
                    </div>
                </Typography>
                <TextField 
                    id="danceability"
                    type="number"
                    defaultValue={danceability}
                    inputProps={{min:0, max:10}}
                    onChange={handleDanceability}
                />
            </FormControl>
        </Grid>
        <Grid item xs={12} align="left">
            <FormControl component="fieldset">
                <Typography component='h6' variant='h6'>
                    <div align='left'>
                        Do you prefer energetic music? Give a rating from 0 to 10. 0 indicates low energy, 10 indicates high energy.
                    </div>
                </Typography>
                <TextField 
                    id="energy"
                    type="number"
                    defaultValue={energy}
                    inputProps={{min:0, max:10}}
                    onChange={handleEnergy}
                />
            </FormControl>
        </Grid>
        <Grid item xs={12} align="left">
            <FormControl component="fieldset">
                <Typography component='h6' variant='h6'>
                    <div align='left'>
                        Do you prefer happy music? Give a rating from 0 to 10. 0 indicates sad music, 10 indicates happy music.
                    </div>
                </Typography>
                <TextField 
                    id="valence"
                    type="number"
                    defaultValue={valence}
                    inputProps={{min:0, max:10}}
                    onChange={handleValence}
                />
            </FormControl>
        </Grid>
        <Grid item xs={12} align="left">
            <FormControl component="fieldset">
                <Typography component='h6' variant='h6'>
                    <div align='left'>
                        Indicate preferred beats per minute for your music recommendations.
                    </div>
                </Typography>
                <TextField 
                    id="tempo"
                    type="number"
                    defaultValue={tempo}
                    inputProps={{min:80, max:140}}
                    onChange={handleTempo}
                />
            </FormControl>
        </Grid>
        <Grid item xs={6} align="center">
            <Button color="primary" variant="contained" onClick={handleSaveButtonPressed}>
                Save
            </Button>
        </Grid>
        <Grid item xs={6} align="center">
            <Button color="secondary" variant="contained" to='/' component={Link}>
                Back
            </Button>
        </Grid>
    </Grid>

    

};