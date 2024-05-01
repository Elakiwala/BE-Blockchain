package blockchain;

//import java.lang.reflect.Array;
import blockchain.Transactions;
//import HashUtil.HashUtil;
import java.util.List;
import java.util.Arrays;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Block
 */
public class Block {

    public int index;
    public String previousHash;
    public Timestamp timestamp;
    public int nbTransactions;
    public ArrayList<Transactions> transactions;
    //public ArrayList<String> merkleTree; // premier item = root hash
    public String merkleRoot;
    public String blockHash;
    public int nonce = 0;
    public String miner;

    public Block(int index,String previousHash, ArrayList<Transactions> transactions,String miner) {
        this.index = index; // hauteur dans la blockchain
        this.previousHash = previousHash;
        this.timestamp = new Timestamp(System.currentTimeMillis());
    //    System.out.println(timestamp);
        this.transactions = transactions;
        this.nbTransactions = transactions.size();
        this.merkleTree(this.transactions);
        this.blockHash = calculateHash();
        this.miner = miner;
    }

    public String getPreviousHash() {
        return previousHash;
    }

    public ArrayList<Transactions> getTransaction() {
        return transactions;
    }

    public String getBlockHash() {
        return blockHash;
    }
    
    public int getIndex() {
        return index;
    }
    
    public void printBlock(){
        System.out.println("Block numéro (Index) : "+index);
        System.out.println("Previous hash : "+previousHash);
        System.out.println("Current hash : "+blockHash);
        System.out.println("Timestamp : "+timestamp);
        System.out.println("Nb transactions : "+nbTransactions);
        System.out.println("Liste des tx :");
        for (int i=0;i<nbTransactions;i=i+1)
            transactions.get(i).printTrans();
        System.out.println(" Merkle tree root : "+merkleRoot);
        System.out.println(" Miner : "+miner);
        System.out.println(" Nonce : "+nonce);
        System.out.println("--------------");
    }
    
    public String calculateHash() {
        String calculatedhash = HashUtil.applySha256( 
            Long.toString(index)+timestamp+transactions+previousHash+nonce+merkleRoot+miner
         );
        return calculatedhash;
    }
    
    public void mineBlock(int difficulty,String minerName) {
        // nom du mineur en paramètre
        // le mineur fabrique le bloc et le mine
        // c'est vérifié (concensus) et ajouté à la BC
        String target = new String(new char[difficulty]).replace('\0', '0');
        while(!blockHash.substring(0, difficulty).equals(target)) {
            this.nonce ++;
            this.blockHash = calculateHash();
        }
        System.out.print("Block Mined!!! : " + blockHash);
        System.out.print(" Block n° : " + index);
        System.out.println(" Nonce = " + nonce);
    }
    
    public boolean verifyBlock(Block blk){
        String hashControl = blk.calculateHash();
        if (blk.blockHash.equals(hashControl))
            return true;
        else{
            System.out.println("Bad block... que fait la police !");
            return false;
        }
    }
    
    public void merkleTree(ArrayList<Transactions> txList) {
        // 
        int count = 0 ;
        ArrayList<String> hashList = new ArrayList<>();

        for (int i=0;i<txList.size();i++){
            String hashElt = HashUtil.applySha256(txList.get(i).stringify());
            hashList.add(i,hashElt);
            }
        //System.out.println(" Nb tx : "+txList.size());
        count = count + hashList.size();
        ArrayList<String> hashTree = new ArrayList<>(hashList);//pile

        while (hashList.size()>1){
            if (hashList.size()%2==1){
                hashList.add(hashList.get(hashList.size()-1));
                hashTree.add(hashTree.get(hashTree.size()-1));
            }
            ArrayList<String> hashList2 = new ArrayList<>(); // vide
            for (int i=0;i<hashList.size();i=i+2){
                String newHash = HashUtil.applySha256(hashList.get(i)+hashList.get(i+1));
                hashList2.add(newHash); // à la fin
                hashTree.add(0,newHash); // au début
                count++;
           }
            hashList = hashList2;
       }
       //merkleTree = hashTree;
       merkleRoot = hashTree.get(0);
       //System.out.println("Nb noeuds : "+count);
    }
}

