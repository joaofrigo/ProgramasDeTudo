var teste
var teste2


/*teste2 = [1,2,3];
console.log(teste2);
teste = teste2[5];
console.log(teste);*/

var variavel = "abc"
var variavel2 = ['a','b','c'];
//variavel2 = "" + variavel2;
//variavel2 = variavel2.toString();
//variavel2 = String(variavel2);
// todos esses métodos consideram as vírgulas dentro do objeto.
teste = typeof(variavel);
teste2 = typeof(variavel2);
console.log("variavel é", variavel, "do tipo", teste, "\n","variavel 2 é", variavel2,"do tipo", teste2);
var stringo = ColocaVirgulas("abc");
//console.log(stringo);


function ColocaVirgulas(stringo)
{
    console.log ("A string é:", stringo);
  stringo = stringo.split('');
  console.log("A string tomou split:", stringo, typeof(stringo));
  stringo = stringo.toString();
  console.log("A string virou string:", stringo, typeof(stringo));
}
