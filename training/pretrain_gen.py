from tqdm.auto import tqdm

def pretrain_gen(gen, dataloader, opt, criterion, device, epochs=5):
    loss_list = []
    
    for epoch in range(epochs):
        for data in tqdm(dataloader):

            L = data['L'].to(device)
            ab = data['ab'].to(device)

            opt.zero_grad()

            preds = gen(L)
            loss = criterion(ab, preds)

            loss.backward()
            opt.step()

            loss_list.append(loss.item())
        print(f"Epoch: {epoch+1} , Loss: {loss_list[-1]}")
    return gen, opt, loss_list