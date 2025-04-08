const fs = require('fs')
const data = fs.readFileSync('./itemids.txt', 'utf8')


catagories = data.split(':\r\n')

//console.log(catagories[2])

var output

catagories[6].split("\r\n").forEach(row => {
    output += `ERItemData("${row.slice(row.indexOf(':') + 2, row.length)}", ${row.slice(4, row.indexOf(':'))}, ERItemCategory.WEAPON),\n`
})

console.log(output)
fs.writeFileSync('./WEAPON.txt', output)