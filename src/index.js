import fs from 'fs'
import _ from 'lodash'

fs.readFile('./data/instances.json', 'utf8', (err, data) => {
  const json = JSON.parse(data)
  const soluce = {}
  for (let i = 1; i <= 10; i++) {
    const maison = json[i]
    // maison.items
    // maison.capacity
    if (i === 1) console.log({ maison })
    // rentabilité massique : prix par kilo
    const rM = maison.values.map((valeurObjet, i) => {
      return valeurObjet / maison.weights[i]
    })
    if (i === 1) console.log({ rM })
    // indexes to sort
    const indexes = []
    for (let j = 0; j < maison.items; j++) {
      indexes.push(j)
    }
    if (i === 1) console.log({ indexes })
    const indexes2 = [...indexes]
    // sort
    indexes2.sort((a, b) => {
      return (rM[b] - rM[a])
    })
    if (i === 1) console.log({ indexes2 })

    // indexes of more expensive per kilo first
    const solutionMaison = new Array(maison.items)
    let poidRestant = maison.capacity
    const maisonSolution = indexes2.map(k => {
      const poid = maison.weights[k]
      if (i === 1) console.log({ poid })
      if (poid <= poidRestant) {
        poidRestant -= poidRestant
        solutionMaison[k] = true
      } else {
        solutionMaison[k] = false
      }
    })
    if (i === 1) console.log({ solutionMaison })
    for (let l = 0; l < maison.items; l++) {
      if (solutionMaison[l] && i === 1) {
        console.log(l)
      }
    }
    // solutionMaison.find

    soluce[i] = solutionMaison
  }
  console.log({ soluce })
  fs.writeFile('./output/solution.json', JSON.stringify(soluce), err => console.log(err))
})
