
var SDR = require('../core/SDR')
var Load = require('../util/Load')
var Partition = require('../util/Partition')

function createWrapper(container){
    const wrap = document.createElement('div')
    wrap.className = 'viz-container'
    container.appendChild(wrap)
    return wrap
}

function createCanvas(container,width,height){
    const canvas = document.createElement('canvas')
    canvas.width = width
    canvas.height = height
    container.appendChild(canvas)
    return canvas
}

module.exports = {

    printSDR({container=document.body,width=900,height=5,arr,indices,range,sdr,title} = {}){
        var sdr = sdr || new SDR({indices,range})
        if(arr)
            sdr.fromBinaryArray(arr)
        const wrap = createWrapper(container)
        wrap.innerHTML += '<span><b>Range:</b> ' + sdr.range + '</span>'
        wrap.innerHTML += '<span><b>Population:</b> ' + sdr.population() + '</span>'
        wrap.innerHTML += '<span><b>Density:</b> ' + sdr.density() + '</span>'
        wrap.innerHTML += '<span><b>Indicies:</b> [' + sdr.indices.join(', ') + ']</span>'
        if(title)
            wrap.innerHTML += '<span><b>Title:</b> ' + title + '</span>'
        wrap.innerHTML += '<br>'
        const canvas = createCanvas(wrap,width,height)
        const depth = sdr.depth()
        const depthMap = sdr.depthMap()
        arr = sdr.toBinaryArray()
        const ctx = canvas.getContext('2d')
        for(var i = 0; i < arr.length; i++){
            ctx.fillStyle = arr[i] ? 'rgba(0,0,0,'+(depthMap[i]/depth)+')' : 'white'
            ctx.fillRect(i*4,0,4,height)
        }
    },

    printImagePartition({container=document.body,width,height,image,windowSize,stepSize,margin=4,scale=1,callback}){
        var wrapper = createWrapper(container)
        const imageData = Load.imageDataGrayscale(image)
        const ctx = createCanvas(wrapper,width,height).getContext('2d')
        const partitions = Partition.matrix({matrix:imageData,windowSize,stepSize,callback: (pixel,xi,yi,x,y) => {
            ctx.fillStyle = pixel == 0 ? 'black' : 'white'
            var px = ((xi * ((windowSize-stepSize) + margin))+x) * scale
            var py = ((yi * ((windowSize-stepSize) + margin))+y) * scale
            ctx.fillRect(px,py,scale,scale)
        }})
    },

    printPartitions({container=document.body,width,height,partitions,callback}){
        var wrapper = createWrapper(container)
        const ctx = createCanvas(wrapper,width,height).getContext('2d')
        for(var y = 0; y < partitions.length; y++){
            for(var x = 0; x < partitions[y].length; x++){
                if(callback)
                    callback(partitions[y][x],x,y,ctx)
            }
        }
    }

}