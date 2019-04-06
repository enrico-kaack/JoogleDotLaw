import axios from "axios";

export default {
    getNormText(norm) {
        return axios.get('/normText/' + norm)
            .then(response => {
                return response.data
            })
    },

    getNormSuggestion(normSuggestion) {
        return axios.get('/normSuggestion/' + normSuggestion)
            .then(response => {
                return response.data
            })
    },

    getResults(searchtext, norm) {
        return axios.get('/search/', {
            params: {
                query: searchtext,
                norm: norm
            }
        })
            .then(response => {
                return response.data
            })
    }
}

