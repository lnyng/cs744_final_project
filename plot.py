from zplot import *

def guess_interval(x):
    import math
    div = int(10**(int(math.log10(x))-1))
    return max(2, int(x)/5/div*div)

def ceil_and_interval(x):
    interval = guess_interval(x)
    return int(math.ceil(x/interval)*interval), interval

def producer():
    t = table('plot2.data', separator=',')
# acks batch_size flush_messages flush_ms latency linger num_producers num_records partition record_size replica throughput

    c = canvas(title='producer_partitions', canvas_type='pdf')
    ymax = t.getmax('throughput')
    ymax, yinterval = ceil_and_interval(ymax*1.2)
    d = drawable(c, xrange=[-0.5,4.5], yrange=[0,ymax])
    axis(d, xtitle='Partitions', xmanual=[[1, 0],[6, 1],[12, 2],[18, 3], [24, 4]],
            ytitle='Throughput (MB/s)', yauto=[0,ymax,yinterval],
            xlabelfontsize=7, ylabelfontsize=7, xtitlesize=7, ytitlesize=7,
            title='Producer Throughput at Different Replication Factors',
            titlesize=7)
    l = legend()

    r1 = table(table=t, where='replica = 1')
    p = plotter()
    p.verticalbars(drawable=d, table=r1, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='blue', barwidth=0.8,
            labelfield='latency_95', cluster=[0,3],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Replicas 1')

    r3a = table(table=t, where='replica = 3 and acks = 1')
    p = plotter()
    p.verticalbars(drawable=d, table=r3a, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='red', barwidth=0.8,
            labelfield='latency_95', cluster=[1,3],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Async Replicas 3')

    r3 = table(table=t, where='replica = 3 and acks = -1')
    p = plotter()
    p.verticalbars(drawable=d, table=r3, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='green', barwidth=0.8,
            labelfield='latency_95', cluster=[2,3],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Replicas 3')

    l.draw(canvas=c, coord=d.map([-.4,2300]), fontsize=5, width=3, height=3)
    c.text(anchor='l', coord=[d.left(),d.bottom()-30], text='*number in parentheses are latency in ms', size=4)
    c.render()

    t = table('plot1.data', separator=',')

    c = canvas(title='producer_record_and_batch_size', canvas_type='pdf')
    ymax = t.getmax('throughput')
    ymax, yinterval = ceil_and_interval(ymax*1.5)
    d = drawable(c, xrange=[-0.5,2.5], yrange=[0,ymax])
    axis(d, xtitle='Record Size (byte)', xmanual=[[128, 0],[256, 1],[512, 2]],
            ytitle='Throughput (MB/s)', yauto=[0,ymax,yinterval],
            ylabelfontsize=7, xlabelfontsize=7, xtitlesize=7, ytitlesize=7,
            title='Producer Throughput')

    l = legend()

    bs1 = table(table=t, where='batch_size = 4096')
    p = plotter()
    p.verticalbars(drawable=d, table=bs1, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='blue', barwidth=0.8,
            labelfield='latency_95', cluster=[0,4],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Batch Size 4k')

    bs2 = table(table=t, where='batch_size = 16384')
    p = plotter()
    p.verticalbars(drawable=d, table=bs2, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='red', barwidth=0.8,
            labelfield='latency_95', cluster=[1,4],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Batch Size 16kB')

    bs3 = table(table=t, where='batch_size = 65536')
    p = plotter()
    p.verticalbars(drawable=d, table=bs3, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='green', barwidth=0.8,
            labelfield='latency_95', cluster=[2,4],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Batch Size 64kB')

    bs4 = table(table=t, where='batch_size = 131072')
    p = plotter()
    p.verticalbars(drawable=d, table=bs4, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='yellow', barwidth=0.8,
            labelfield='latency_95', cluster=[3,4],
            labelsize=4,  labelformat='(%s)', labelrotate=90,   labelanchor='l,l',
            legend=l, legendtext='Batch Size 128kB')

    l.draw(canvas=c, coord=d.map([-0.40,660]), fontsize=4, width=3, height=2)
    c.text(anchor='l', coord=[d.left(),d.bottom()-30], text='*number in parentheses are latency in ms', size=4)
    c.render()

def consumer():
    t = table('plot3.data', separator=',')

    c = canvas(title='consumer_partitions', canvas_type='pdf')
    ymax = t.getmax('throughput')
    ymax, yinterval = ceil_and_interval(ymax)
    d = drawable(c, xrange=[-0.5,4.5], yrange=[0,ymax])
    axis(d, xtitle='Partitions', xmanual=[[1, 0],[6, 1],[12, 2],[18, 3], [24, 4]],
            ytitle='Throughput (MB/s)', yauto=[0,ymax,yinterval],
            xlabelfontsize=7, ylabelfontsize=7, xtitlesize=7, ytitlesize=7,
            title='Consumer Throughput')
    l = legend()

    r1 = table(table=t, where='replica = 1')
    p = plotter()
    p.verticalbars(drawable=d, table=r1, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='blue', barwidth=0.8,
            cluster=[0,2],
            legend=l, legendtext='Replicas 1')

    r3 = table(table=t, where='replica = 3')
    p = plotter()
    p.verticalbars(drawable=d, table=r3, xfield='rownumber', yfield='throughput',
            fill=True, fillcolor='red', barwidth=0.8,
            cluster=[1,2],
            legend=l, legendtext='Replicas 3')

    l.draw(canvas=c, coord=d.map([-.4,1000]), fontsize=5, width=3, height=3)
    c.text(anchor='l', coord=[d.left(),d.bottom()-30], text='*number in parentheses are latency in ms', size=4)
    c.render()

if __name__ == '__main__':
    producer()
    consumer()
