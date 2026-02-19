<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini Netflix</title>

<style>
body{
  margin:0;
  font-family:Arial, Helvetica, sans-serif;
  background:#111;
  color:white;
}

header{
  background:black;
  padding:15px 30px;
  font-size:24px;
  font-weight:bold;
  color:red;
}

.section{
  padding:20px;
}

.movie-row{
  display:flex;
  overflow-x:auto;
  gap:15px;
  scroll-behavior:smooth;
}

.movie-card{
  min-width:180px;
  background:#222;
  border-radius:10px;
  padding:10px;
  transition:0.3s;
}

.movie-card:hover{
  transform:scale(1.05);
}

.poster{
  width:100%;
  height:250px;
  background:#333;
  border-radius:8px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:14px;
  text-align:center;
  padding:10px;
}

button{
  margin-top:8px;
  width:100%;
  padding:6px;
  border:none;
  border-radius:5px;
  cursor:pointer;
  font-weight:bold;
}

.add{
  background:red;
  color:white;
}

.remove{
  background:#555;
  color:white;
}

.nav{
  display:flex;
  gap:20px;
  padding:10px 30px;
  background:#1a1a1a;
}

.nav span{
  cursor:pointer;
}

.active{
  color:red;
}

.hidden{
  display:none;
}
</style>
</head>

<body>

<header>Mini Netflix</header>

<div class="nav">
  <span id="homeBtn" class="active">Home</span>
  <span id="watchlistBtn">❤️ My Watchlist</span>
</div>

<div id="homeSection" class="section">
  <h2>🔥 Popular Movies</h2>
  <div class="movie-row" id="movieRow"></div>
</div>

<div id="watchlistSection" class="section hidden">
  <h2>❤️ My Watchlist</h2>
  <div class="movie-row" id="watchlistRow"></div>
</div>

<script>

const movies = [
"Interstellar","Inception","The Dark Knight","Titanic",
"Avengers: Endgame","The Matrix","Joker","Parasite",
"Top Gun: Maverick","Oppenheimer",
"ฉลาดเกมส์โกง","พี่มาก..พระโขนง","แฟนฉัน",
"ร่างทรง","ชัตเตอร์ กดติดวิญญาณ",
"John Wick","The Conjuring","Dune","Barbie","Frozen"
];

let watchlist = JSON.parse(localStorage.getItem("watchlist")) || [];

function saveWatchlist(){
  localStorage.setItem("watchlist", JSON.stringify(watchlist));
}

function renderMovies(){
  const row = document.getElementById("movieRow");
  row.innerHTML="";
  movies.forEach(movie=>{
    const card = document.createElement("div");
    card.className="movie-card";

    const isAdded = watchlist.includes(movie);

    card.innerHTML=`
      <div class="poster">${movie}</div>
      <button class="${isAdded?'remove':'add'}"
        onclick="toggleWatchlist('${movie}')">
        ${isAdded?'Remove':'Add to Watchlist'}
      </button>
    `;

    row.appendChild(card);
  });
}

function renderWatchlist(){
  const row = document.getElementById("watchlistRow");
  row.innerHTML="";
  if(watchlist.length===0){
    row.innerHTML="<p>ยังไม่มีหนังใน Watchlist</p>";
    return;
  }

  watchlist.forEach(movie=>{
    const card = document.createElement("div");
    card.className="movie-card";

    card.innerHTML=`
      <div class="poster">${movie}</div>
      <button class="remove"
        onclick="toggleWatchlist('${movie}')">
        Remove
      </button>
    `;

    row.appendChild(card);
  });
}

function toggleWatchlist(movie){
  if(watchlist.includes(movie)){
    watchlist = watchlist.filter(m=>m!==movie);
  }else{
    watchlist.push(movie);
  }
  saveWatchlist();
  renderMovies();
  renderWatchlist();
}

document.getElementById("homeBtn").onclick=()=>{
  document.getElementById("homeSection").classList.remove("hidden");
  document.getElementById("watchlistSection").classList.add("hidden");
  homeBtn.classList.add("active");
  watchlistBtn.classList.remove("active");
};

document.getElementById("watchlistBtn").onclick=()=>{
  document.getElementById("homeSection").classList.add("hidden");
  document.getElementById("watchlistSection").classList.remove("hidden");
  watchlistBtn.classList.add("active");
  homeBtn.classList.remove("active");
};

renderMovies();
renderWatchlist();

</script>

</body>
</html>
