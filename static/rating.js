const ratingDiv = document.querySelector('.best-players tbody')

async function getBestPlayers() {
    let data = await fetch('http://localhost:5000/rating')
    return data.json()
}

document.addEventListener('DOMContentLoaded', async () => {
    const data = await getBestPlayers()
    for (let i in data) {
        let row = document.createElement('tr')

        let rankCell = document.createElement('td')
        rankCell.textContent = Number(i) + 1
        row.appendChild(rankCell)

        let nameCell = document.createElement('td')
        nameCell.textContent = data[i].name
        row.appendChild(nameCell)

        let pointsCell = document.createElement('td')
        pointsCell.textContent = data[i].total_point
        row.appendChild(pointsCell)

        ratingDiv.appendChild(row)
    }
})
