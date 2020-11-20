import fs from 'fs'
import _ from 'lodash'
console.log('======================== read text ======')
fs.readFile('./data/dataset1.txt', 'utf8', (err, data) => {
  if (err) {
    console.log({ err })
    return
  }
  console.log({ data })
})

console.log('=================== parse a json =====')
fs.readFile('./data/json1.txt', 'utf8', (err, data) => {
  if (err) {
    console.log({ err })
    return
  }
  const json = JSON.parse(data)
  console.log({ json })
  console.log(typeof json)
  console.log({ 'json.array': _.get(json, 'array') })
})
