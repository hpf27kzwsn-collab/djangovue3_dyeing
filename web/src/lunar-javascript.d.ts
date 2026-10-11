declare module 'lunar-javascript' {
 export interface LunarDate {getFestivals():string[];getJieQi():string}
 export interface SolarDate {getLunar():LunarDate;getFestivals():string[]}
 export const Solar:{fromDate(date:Date):SolarDate}
}
