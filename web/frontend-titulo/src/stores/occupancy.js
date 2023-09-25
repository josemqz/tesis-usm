import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useOccupancyStore = defineStore('occupancy',{
    state: () => ({
		// objeto axios para hacer HTTP requests al servidor de backend 
        backend: axios.create({ baseURL: 'http://localhost:5000' }),

        ocupaciones_info: [],
        oc_tiempos: [],

        salas: [],

        t_last: new Date(),

        loaded: false,
    }),
    getters: {
        getOcupacionesInfo(state){
            return state.ocupaciones_info;
        },
        getSalas(state){
            return state.salas;
        },
        getLoaded(state){
            return state.loaded;
        }
    },
    actions: {
        async fetchSalas(){
            var response = 
            await this.backend.get('/salas')
            .then(response => {
                return response
            })
            .catch(error => {
                console.error(error)
                throw error
            })
            // console.log("response.data [getSalas]", response.data)  
            this.salas = response.data
            
        },
        
        async fetchOcupaciones() {
            var response =
            await this.backend.get('/ocupaciones')
            .then(response => {
                return response
            })
            .catch(error => {
                console.error(error)
                throw error
            })
            
            this.ocupaciones_info = response.data
            this.ocupaciones_info = this.ocupaciones_info.map( item => { return {...item, tasa_ocupacion:-1}});
            this.oc_tiempos = this.ocupaciones_info.map(({ timestamp }) => new Date(timestamp));
            
            // console.log("ocupaciones_info:", this.ocupaciones_info, "tipo:", typeof(this.ocupaciones_info))
            // console.log("tiempos:", this.oc_tiempos)
        },
    
        async setTasasOcupacion(){
            await this.fetchOcupaciones();
            await this.fetchSalas();
        
            // obtener timestamp más temprana y más tardía y mostrar // no es necesario, mejor mostrar hora de cada detección
            this.t_last = new Date(Math.max.apply(null, this.oc_tiempos.map(function(e) {
                // console.log(e)
                // console.log(e.getTime())
                return e.getTime();
            })));
        
            console.log("tiempo más reciente:", this.t_last)
        
            try {
                // var index = 0
                this.ocupaciones_info = this.ocupaciones_info.map((item) => {
                    
                    try {
                        var ocupacion_max = this.salas.find(salas_item => salas_item.id === item.sala_id).ocupacion_max

                        console.log("\n - - - ")
                        
                        console.log(`(${item.sala_id},${this.salas.find(salas_item => salas_item.id === item.sala_id).nombre}): 
                                    ocupacion: ${item.ocupacion_actual}, 
                                    maxOcupacion: ${ocupacion_max}`);
                        
                        
                        console.log("exito")
                        return {...item, tasa_ocupacion: item.ocupacion_actual/ocupacion_max};
                    } catch (error) {
                        console.log("fracaso", error)
                        return {...item};
                    }
                });
        
                
                console.log("\n- - - - - - - \nTasas de ocupacion:")
                console.log(this.ocupaciones_info)
                
            } catch (error) {
                console.error(error)
            }

            // indicar que terminó el procesamiento de datos
            this.loaded = true
        }
    },
})
