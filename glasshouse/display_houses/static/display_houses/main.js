const cityForm = document.getElementById('city-form')
const cityMenu = document.getElementById('city-menu')
const districtMenu = document.getElementById('district-menu')

$.ajax({
    type: 'GET',
    url: '/city-json',
    success: function(response){
        console.log(response.data)
        const cityData = response.data
        cityData.map(item=>{
            const option = document.createElement('option')
            option.textContent = item.name
            option.setAttribute('value', item.name)
            cityMenu.appendChild(option)
        })
    },
    error: function(error){
        console.log(error.data)
    }
})

cityMenu.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedCity = e.target.value
    districtMenu.innerHTML = ""

    // reset to Choose District when city changed
    const default_option = document.createElement('option')
    default_option.textContent = "Choose District"
    default_option.setAttribute('hidden', "")
    default_option.setAttribute('value', "")
    districtMenu.append(default_option)

    $.ajax({
        type: 'GET',
        url: `district-json/${selectedCity}`,
        success: function(response){
            console.log(response.data)
            districtData = response.data
            districtData.map(item=>{
                const option = document.createElement('option')
                option.textContent = item.name
                option.setAttribute('value', item.name)
                districtMenu.append(option)
            })

        },
        error: function(error){
            console.log(error.data)
        }

    })
})

// function getSelected(){
//     const selectedCity = "Taipei City"
//     document.write(selectedCity)
//     console.log("from getSelected!")
// }