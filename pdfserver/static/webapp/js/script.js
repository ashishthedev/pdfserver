
function JSDateToUnixTime(jsDate){
  return Math.floor(jsDate.getTime()/1000);
}

function DDMMMYYFromUnixTime(unixTime){
  return DateAsUnixTimeToDDMMMYY(unixTime);
}

function DateAsUnixTimeToDDMMMYY(unixTime) {
  var d = new Date(unixTime);

  function pad2(n) {
    return n > 9 ? n : '0' + n;
  }

  var MONTH_AS_TEXT = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
  }
  var d = new Date(unixTime*1000);
  var year = d.getUTCFullYear();
  var month = MONTH_AS_TEXT[d.getUTCMonth() + 1];  // months start at zero

  var day = d.getUTCDate();

  return pad2(day) + month + year;
}

function GetDateDiffAsText(JSDate){
  var today = new Date();
  var diff = Math.floor(today.getTime()/1000 - JSDate.getTime()/1000);
  var day = 60 * 60 * 24;

  var days = Math.floor(diff/day);

  var dateDiffFromTodayAsText = "";
  if (days == 0) {
    dateDiffFromTodayAsText = "Today";
  }
  else if (days == 1) {
    dateDiffFromTodayAsText = "1 day old";
  } else {
    dateDiffFromTodayAsText = days + " days old";
  }
  return dateDiffFromTodayAsText;

}

function UpdateDateDiffAsText($scope) {
  $scope.dateDiffFromTodayAsText = GetDateDiffAsText($scope.dateValue);
}

function Debug(){
  //return true;
  return false;
}


function DefaultSuppliersList(){
  return ["Standard", "Omega"];
}

function DefaultBillingCategories(){
  return ["Central", "UP", "Jobwork", "Export", "Tracking"];
}
function DefaultCaseTypes(){
  return ["Straight", "Taper"];
}

function DefaultPelletSizes() {
  return ["10x08", "13x10", "15x13", "17x15", "19x17", "22x18", "25x20", "30x24", "35x24"];
}

function DefaultCaseSizes() {
  return ["28x16", "28x20", "38x26", "40x28", "43x28", "50x35", "53x35", "70x40"];
}

function numberToEnglish( n ) {

    var string = n.toString(), units, tens, scales, start, end, chunks, chunksLen, chunk, ints, i, word, words, and = 'and';

    /* Is number zero? */
    if( parseInt( string ) === 0 ) {
        return 'zero';
    }

    /* Array of units as words */
    units = [ '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen' ];

    /* Array of tens as words */
    tens = [ '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety' ];

    /* Array of scales as words */
    scales = [ '', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion', 'undecillion', 'duodecillion', 'tredecillion', 'quatttuor-decillion', 'quindecillion', 'sexdecillion', 'septen-decillion', 'octodecillion', 'novemdecillion', 'vigintillion', 'centillion' ];

    /* Split user arguemnt into 3 digit chunks from right to left */
    start = string.length;
    chunks = [];
    while( start > 0 ) {
        end = start;
        chunks.push( string.slice( ( start = Math.max( 0, start - 3 ) ), end ) );
    }

    /* Check if function has enough scale words to be able to stringify the user argument */
    chunksLen = chunks.length;
    if( chunksLen > scales.length ) {
        return '';
    }

    /* Stringify each integer in each chunk */
    words = [];
    for( i = 0; i < chunksLen; i++ ) {

        chunk = parseInt( chunks[i] );

        if( chunk ) {

            /* Split chunk into array of individual integers */
            ints = chunks[i].split( '' ).reverse().map( parseFloat );

            /* If tens integer is 1, i.e. 10, then add 10 to units integer */
            if( ints[1] === 1 ) {
                ints[0] += 10;
            }

            /* Add scale word if chunk is not zero and array item exists */
            if( ( word = scales[i] ) ) {
                words.push( word );
            }

            /* Add unit word if array item exists */
            if( ( word = units[ ints[0] ] ) ) {
                words.push( word );
            }

            /* Add tens word if array item exists */
            if( ( word = tens[ ints[1] ] ) ) {
                words.push( word );
            }

            /* Add 'and' string after units or tens integer if: */
            if( ints[0] || ints[1] ) {

                /* Chunk has a hundreds integer or chunk is the first of multiple chunks */
                if( ints[2] || ! i && chunksLen ) {
                    words.push( and );
                }

            }

            /* Add hundreds word if array item exists */
            if( ( word = units[ ints[2] ] ) ) {
                words.push( word + ' hundred' );
            }

        }

    }

    return words.reverse().join( ' ' );

}
