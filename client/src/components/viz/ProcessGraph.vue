<template>
    <div class="card p-0 h-100">

        <network ref="network" class="w-100 h-100"
                 :nodes="nodes"
                 :edges="edges"
                 :options="options"
        >
        </network>


    </div>
</template>
<script>
export default {
  name: 'ProcessGraph',
  props: {
    pipes: Array,
  },
  data() {
    return {
      options: {
        nodes: {
          shape: 'dot',
          size: 15,
          borderWidth: 1,
          font: {
            face: 'monospace',
            align: 'left',
            size: 12,
          },
        },
        edges: {
          color: '#656765',
        },
        layout: {
          randomSeed: 42,
          // hierarchical: true,
        },

      },
    };
  },
  computed: {
    nodes() {
      let nodes = [];
      // console.log('this.config', this..pipe_configs);

      this.pipes.forEach(pipe => {
        var node = {
          id: pipe.id,
          label: pipe.name,
        };
        if ('status' in pipe && pipe.status !== null) {
          var title = ''

            + '<div style="font-size:13px; line-height:13px">'
            + pipe.status.replace(/\n/g, '</div><div style="font-size:13px; line-height:13px">')
            + '</div>';
          console.log('from', pipe.status, 'to', title);
          node.title = title;

          console.log('pipe', pipe, 'has status', pipe.status);
          if (pipe.status === 'Complete') {
            node.color = '#8fd9a8';
          } else if (pipe.status.toLowerCase()
            .includes('error')) {
            node.color = '#d9241f';
            // node.font.color = '#fffefb';

          } else {
            node.color = '#88b4d9';
          }
        }
        nodes.push(node);
      });
      return nodes;
    },
    edges() {
      let edges = [];
      this.pipes.forEach(pipe => {
        if ('dependencies' in pipe) {
          pipe.dependencies.forEach(dep => {
            edges.push({
              from: dep,
              to: pipe.id,
              arrows: 'to',
            });
          });
        }
      });
      console.log('edges', edges);
      return edges;
    },
  },
};
</script>
