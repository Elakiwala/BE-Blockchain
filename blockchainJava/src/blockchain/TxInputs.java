/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package blockchain;

import java.util.ArrayList;

/**
 *
 * @author vincent
 */
public class TxInputs {
    public String hash; // hash de l'UTXO source
    public int hauteur; // num du bloc contenant la Tx pour payer, tout à 0 si coinbase input
    public int outIndex;  // la sortie concernée
    public long amount; // montant de l'UTXO source
    public int unlockSize; // nb d'item dans le unlocking script, zéro si coinbase input
    public ArrayList<String> unlockingScript; // 
    public String comment; // coinbase ou autre
    
    public TxInputs(String hash, int hauteur, int outIndex,long amount,int unlockSize,
    ArrayList<String> unlockingScript, String comment) {
 
        this.hauteur = hauteur; // à virer
        this.hash = hash; 
        this.outIndex = outIndex;
        this.amount = amount;
        this.unlockSize = unlockSize;
        this.unlockingScript = unlockingScript;
        this.comment = comment;
    }
    public void print(){
        //System.out.println("--- Input List ---");
        //System.out.print("Hauteur : "+this.hauteur);
        System.out.print(" ; hash : "+this.hash);
        System.out.print(" ; out index : "+this.outIndex);
        System.out.print(" ; Unlock size : "+this.unlockSize);
        System.out.print(" ; unlocking : "+this.unlockingScript);
        System.out.println(" ; Comment : "+this.comment);
    }
}
