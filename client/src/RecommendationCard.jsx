
function RecommendationCard({artwork, artist, album, title, reason, onPlay}){

    const youtubeQuery = "https://www.youtube.com/results?search_query=" + encodeURIComponent(artist + " " + title)

return(
    <div className="border border-amber-400 rounded-xl p-5 bg-linear-to-r from-zinc-900 to-zinc-800 flex flex-col items-center hover:border-zinc-400 transition-colors text-center">
        <p><img src={artwork} alt={artist} /></p>
        <h1 className="text-amber-400 font-bold text-2xl">{artist}</h1>
        <p className="font-bold">{title}</p>        
        <p className="text-sm">{album}</p>
        <p className="text-sm italic">{reason}</p>
        <p className="py-3"><a href={youtubeQuery} target="blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8 text-amber-400 hover:text-amber-300">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
            </svg></a>
        </p>
    </div>
)
}

export default RecommendationCard