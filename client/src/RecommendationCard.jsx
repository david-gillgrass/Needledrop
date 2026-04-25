
function RecommendationCard({artist, album, title, reason}){

return(
    <div className="recCard">
        <h3>{artist}</h3>
        <p>Album: {album}</p>
        <p>Title: {title}</p>
        <p>Reason: {reason}</p>
    </div>
)
}

export default RecommendationCard