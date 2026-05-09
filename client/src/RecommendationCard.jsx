
function RecommendationCard({artwork, artist, album, title, reason, onPlay}){

    const youtubeQuery = "https://www.youtube.com/results?search_query=" + encodeURIComponent(artist + " " + title)

return(
    <div className="border border-amber-400 rounded-xl p-5 bg-linear-to-r from-zinc-900 to-zinc-800 flex flex-col items-center hover:border-zinc-400 transition-colors text-center">
        <p><img src={artwork} alt={artist} /></p>
        <h1 className="text-amber-400 font-bold text-2xl">{artist}</h1>
        <p className="font-bold">{title}</p>        
        <p className="text-sm">{album}</p>
        <p className="text-sm italic">{reason}</p>
        <p className="py-3 flex flex-row justify-items-center align-middle"><a href={youtubeQuery} target="blank" rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8 text-amber-400 hover:text-amber-300">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
            </svg></a>
            <button type="button" className="cursor-pointer pl-1"
            onClick={()=>onPlay(artist, title)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-spotify" viewBox="0 0 16 16">
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.669 11.538a.5.5 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686m.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858m.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288"/>
            </svg></button>
        </p>

    </div>
)
}

export default RecommendationCard