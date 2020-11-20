import fs from 'fs'
import _ from 'lodash'

fs.readFile('./data/instances.json', 'utf8', (err, data) => {
  const json = JSON.parse(data)
  const soluce = {}
  for (let i = 1; i <= 10; i++) {
    const maison = json[i]
    // rentabilité massique : prix par kilo
    const rM = maison.values.map((valeurObjet, i) => {
      return valeurObjet / maison.weights[i]
    })
    // indexes to sort : [0,1,2,...,maison.items]
    const indexes = []
    for (let j = 0; j < maison.items; j++) {
      indexes.push(j)
    }
    // sort objects by decreasing rentability
    indexes.sort((a, b) => {
      return (rM[b] - rM[a])
    })

    const solutionMaison = new Array(maison.items)
    // indexes of more expensive per kilo first
    let poidRestant = maison.capacity
    const maisonSolution = indexes.map(k => {
      const poid = maison.weights[k]
      if (poid <= poidRestant) {
        poidRestant = poidRestant - poid
        solutionMaison[k] = true
      } else {
        solutionMaison[k] = false
      }
    })
    soluce[i] = solutionMaison
  }
  fs.writeFile('./output/solution.json', JSON.stringify(soluce), err => console.log(err))
})
