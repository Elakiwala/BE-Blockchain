/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package blockchain;

import java.sql.Timestamp;
import java.util.ArrayList;

/**
 *
 * @author vincent
 */
public class Transactions {
    public Timestamp timestamp;
    public int nbInputs;
    public ArrayList<TxInputs> lstInputs = new ArrayList<>(); // une ou plusieurs UTXO
    public int nbOutputs;
    public ArrayList<TxOutputs> lstOutputs = new ArrayList<>(); // limité à trois sorties : la tx+reward+change
    // les adresses sont dans les scripts
    public String comment;

    
    public Transactions(String comment) {
        this.timestamp = new Timestamp(System.currentTimeMillis());
        this.comment = comment;
    }
    
    public void printTrans(){
        System.out.println("Nb inputs : "+nbInputs);
        System.out.println("Nb outputs : "+nbOutputs);
        System.out.print("Inputs list :");
        for (int i=0;i<lstInputs.size();i++){
            lstInputs.get(i).print();
        }
        System.out.println();
        System.out.print("Outputs list : ");
        for (int i=0;i<lstOutputs.size();i++){
            lstOutputs.get(i).print();
        }
        System.out.println("Comments : "+comment);
        //System.out.println("--------------");
    }
    
    public void coinbaseTx(long reward, String user){
        ArrayList<String> lockScript = new ArrayList<>();
        lockScript.add("<tx sign "+ user+">");
        lockScript.add("<pubKey "+user+">");
        lockScript.add("DUP");
        lockScript.add("HASH");
        TxOutputs outTx = new TxOutputs(0,"0",lockScript,reward);
        //outTx.print();
        this.lstOutputs.add(outTx);
        this.nbInputs = lstInputs.size();
        this.nbOutputs = lstOutputs.size();
    }
    
    public ArrayList<String> lockScript(String user){
        ArrayList<String> lockScript = new ArrayList<>();
        lockScript.add("<tx sign "+ user+">");
        lockScript.add("<pubKey "+user+">");
        lockScript.add("DUP");
        lockScript.add("HASH");
        return lockScript;
    }
    
    public long fees(){
        long inputAmount = 0;
        long outputAmount = 0;
        for (int i = 0;i<lstOutputs.size();i++)
            outputAmount += lstOutputs.get(i).amount;
        for (int i = 0;i<lstInputs.size();i++)
            inputAmount += lstInputs.get(i).amount;
        return inputAmount - outputAmount;
    }
    
    public ArrayList<TxOutputs> marketTx(ArrayList<TxOutputs> utxoList,String user, String dest,long amount,int feeRate){
        // création d'une tx générale avec inputs et outputs 
        ArrayList<String> unlockScript = new ArrayList<>(); // pour unlocker la tx qui justifie la source financière
        ArrayList<String> lockScript = new ArrayList<>(); // pour locker l'output utxo
        ArrayList<String> lockScriptChange = new ArrayList<>(); // pour locker l'output utxo
        ArrayList<TxOutputs> lstUtxoIn = new ArrayList<>();
        String hashSourceTx = ""; // la tx source de l'argent
        long change = 0,fees,inAmount = 0; // le change, les frais
        long globalInAmount = 0; // somme des imputs 
        int hauteur = 0; // pas géré pour l'instant
        // création du script de lock pour Bob
        lockScript = this.lockScript(dest); // locking script de l'output destinataire
  
        
        // création du script unlock pour la source de'Alice
        unlockScript.add("H(<pubKey "+ user+">)");
        unlockScript.add("EQ");
        unlockScript.add("VER");
        
        // recherche des l'utxo qui vont bien pour justifier la source
        //System.out.println("Tx market");// debug
        fees = amount*(long) feeRate/100; // les frais
        for (TxOutputs utxo : utxoList) {
            //System.out.println("Recherche utxo source : "+utxo.lockingScript);// debug
            if (utxo.verify(unlockScript)){ // c'est bien Alice la propriétaire
                globalInAmount += utxo.amount;
                lstUtxoIn.add(utxo);
                if (globalInAmount >=amount+fees) // on en a assez
                    break;
            }
        }
        change = globalInAmount - amount-fees;
        for (TxOutputs utxo : lstUtxoIn){
            //System.out.println("===> On a trouvé une source : ");utxo.print();// debug
            //System.out.println("------");// debug
            hashSourceTx = utxo.hash;
            inAmount = utxo.amount;
            // script de lock pour le change d'Alice
            lockScriptChange = this.lockScript(user);
            TxInputs inTx = new TxInputs(hashSourceTx, hauteur, 0,inAmount,unlockScript.size(),unlockScript, "market tx");
            this.lstInputs.add(inTx);
            // on supprime de la liste utxo générale celle qui vient d'être consommée
            utxoList.remove(utxo); // renvoyer la liste à la fin
            //break;
        }
        if (this.lstInputs.isEmpty()){
            System.out.println("======> Liste imputs vide... quelque chose à merdé");
        }
        //System.out.println("****** VERIF SOURCE ***** Golbal inAmount : "+inAmount+" Change : "+change+" Fees : "+fees+"LSC.size : "+lockScriptChange.size()); // debug
       
        // création des listes inputs et outputs de la tx
        TxOutputs outChange = new TxOutputs(1,"0",lockScriptChange, change);
        outChange.hash = outChange.calculateHash();
        TxOutputs outTx = new TxOutputs(0,"0",lockScript,amount);
        //outTx.hash = outTx.calculateHash();
        //outChange.hash = outChange.calculateHash();
        if (outTx.lockingScript.isEmpty() || outChange.lockingScript.isEmpty()){
            System.out.println("*** PB ***");
        }
            
        // ajouter la tx, le change en output, les frais sont pour le mineur
        this.lstOutputs.add(outTx); 
        this.lstOutputs.add(outChange);
        this.nbInputs = lstInputs.size();
        this.nbOutputs = lstOutputs.size();
        
        // on ajoute les deux transactions de sortie à la liste utxo
        utxoList.add(outTx);
        utxoList.add(outChange);
        return utxoList;
    }
    
    public String stringify(){
        return timestamp.toString()+nbInputs+lstInputs+nbOutputs+lstOutputs+comment;
    }
}
