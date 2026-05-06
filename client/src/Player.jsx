
function Player({artist,title}){

    const embedURL = `https://widget.deezer.com/widget/dark/search/${encodeURIComponent(artist + " " + title)}`
    console.log(artist)
    return(
        <iframe src= {embedURL} 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            allowFullScreen
            frameBorder="0"
            className="w-full h-48"
        />
    )


}

export default Player