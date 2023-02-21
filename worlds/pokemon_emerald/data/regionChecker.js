const regions = require('./regions.json')

let numErrors = 0

const definedRegions = Object.keys(regions)
Object.entries(regions).forEach(([regionName, region]) => {
  region.exits.forEach((exit) => {
    if (!definedRegions.includes(exit)) {
      console.log(`ERROR: Region [${exit}] referenced by [${regionName}] was not defined`)
      ++numErrors
    }
  })
})

const warpsByClaim = Object.entries(regions).reduce((acc, [regionName, region]) => {
  return [...acc, ...region.warps.map((warp) => [regionName, warp])]
}, [])
const warps = warpsByClaim.map(([_, warp]) => warp)

const warpsMatch = (warp1, warp2) => {
  const [from1, to1] = warp1.split('/')
  const [from2, to2] = warp2.split('/')

  const [fromMap1, fromIndices1] = from1.split(':')
  const [toMap1, toIndex1] = to1.split(':')
  const [fromMap2, fromIndices2] = from2.split(':')
  const [toMap2, toIndex2] = to2.split(':')

  return fromMap1 === toMap2 &&
         toMap1 === fromMap2 &&
         fromIndices1.split(',').includes(toIndex2) &&
         fromIndices2.split(',').includes(toIndex1)
}

warps.forEach((warp) => {
  const numClaimants = warpsByClaim.reduce((acc, [claimant, claimedWarp]) => acc + (warp === claimedWarp ? 1 : 0), 0)
  if (numClaimants > 1) {
    console.log(`ERROR: Warp [${warp}] was claimed by more than one region`)
    ++numErrors
  }

  if (!warps.some((otherWarp) => warpsMatch(warp, otherWarp))) {
    console.log(`WARN: Warp [${warp}] looks like a one-way warp`)
    ++numErrors
  }
})

console.log(`Found ${numErrors} problem${numErrors === 1 ? '' : 's'}`)
