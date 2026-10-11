export const pages=import.meta.glob(['./pages/**/*.vue','./plugins/**/*.vue'])
export const componentNames=['system/Resource',...Object.keys(pages).map(path=>path.slice(2,-4))]
