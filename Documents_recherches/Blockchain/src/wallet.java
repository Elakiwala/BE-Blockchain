
import blockchain.TxOutputs;
import java.util.ArrayList;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author vincent
 */
public class wallet {
    public ArrayList<TxOutputs> utxoList;
    public int totalAmount; // in satoBnb
    public String pubKey;
    public String privKey;


public wallet(String str){
    this.utxoList = new ArrayList<>();
    this.pubKey = "pubKey"+str;  
    this.privKey = "privKey"+str;
    this.totalAmount = 0;
}

public int totalAmount(){
    int som = 0;
    for (int i = 0 ; i<utxoList.size();i++){
        som += utxoList.get(i).amount;
    }
    this.totalAmount = som;
    return som;
}
}