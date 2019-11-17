
// From https://stackoverflow.com/questions/43208012/how-do-i-format-currencies-in-a-vue-component
export function toUSD(value) {
    if (typeof value !== "number") {
        return value;
    }
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    });
    return formatter.format(Math.round(value)); // in MealsCount, we are not concerned with the cents
};

export function toCount(value){
    if (typeof value !== "number") {
        return value;
    }
    var formatter = new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0
    });
    return formatter.format(value);

};