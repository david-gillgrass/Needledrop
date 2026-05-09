
function Player({ trackID }){
    
    const spotifyTrack = "https://open.spotify.com/embed/track/"+ trackID
    
    return(
    <div className="pb-2">
    <iframe
    src = {spotifyTrack}
    width="100%" 
    height="152" 
    frameBorder="0" 
    allowfullscreen="" 
    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
    loading="lazy"/>
    </div>
    )


}

export default Player